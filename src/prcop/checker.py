import json
import logging
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError
from pathlib import Path

from .alerts import ReviewOverdueAlert
from .business_hours import business_hours_between_dates, within_business_hours
from .config import Config
from .exceptions import FailedToGetData
from .http_client import HttpClient


logger = logging.getLogger(__name__)


class PullRequest:

    _MIN_TIME_SINCE_UPDATED = timedelta(hours=3)
    _MIN_APPROVALS = 2

    def __init__(self, data, *, repo, record):
        self._data = data
        self._repo = repo
        self._record = record

    def alerts(self):
        id_str = f"{self._repo.full_slug}#{self._id}"
        logger.debug(f"{id_str} is labeled work in progress: {self._labeled_work_in_progress}")
        logger.debug(f"{id_str} business hours since updated: {self.business_hours_since_updated}")
        logger.debug(f"{id_str} recently alerted: {self._recently_alerted}")
        logger.debug(f"{id_str} reviews remaining: {self.reviews_remaining}")
        logger.debug(f"{id_str} needs work: {self._needs_work}")
        if (
            self.business_hours_since_updated >= self._MIN_TIME_SINCE_UPDATED
            and not self._labeled_work_in_progress
            and not self._recently_alerted
            and self.reviews_remaining
            and not self._needs_work
        ):
            self._record.record_alert(self._id)
            return [ReviewOverdueAlert(self)]
        return []

    @property
    def reviews_remaining(self):
        return max(self._MIN_APPROVALS - self._approvals, 0)

    @property
    def _id(self):
        return str(self._data["id"])

    @property
    def title(self):
        return self._data["title"]

    @property
    def _labeled_work_in_progress(self):
        return self.title.startswith("WIP")

    @property
    def _recently_alerted(self):
        return self._record.alerted_recently(self._id)

    @property
    def _approvals(self):
        return sum(review["status"] == "APPROVED" for review in self._data["reviewers"])

    @property
    def _needs_work(self):
        return any(review["status"] == "NEEDS_WORK" for review in self._data["reviewers"])

    @property
    def business_hours_since_updated(self):
        return business_hours_between_dates(
            datetime.fromtimestamp(self._data["updatedDate"] / 1000), datetime.now()
        )

    @property
    def url(self):
        return (
            f"{self._repo.base_url}/projects/{self._repo.project_slug}/"
            f"repos/{self._repo.slug}/pull-requests/{self._id}/"
        )


class Repo:
    def __init__(self, base_url, project, repo, *, record, http):
        self.base_url = base_url
        self.project_slug = project
        self.slug = repo
        self._record = record
        self._http = http

    def alerts(self):
        url = (
            f"{self.base_url}/rest/api/1.0/projects/{self.project_slug}"
            f"/repos/{self.slug}/pull-requests"
        )
        api_response = self._http.get(url)
        try:
            prs = api_response.json()["values"]
        except (JSONDecodeError, KeyError):
            raise FailedToGetData(
                f"{self.full_slug} failed to return pr data: {api_response.text}"
            )
        alerts = []
        for pr_data in prs:
            pr = PullRequest(pr_data, repo=self, record=self._record)
            alerts += pr.alerts()
        return alerts

    @property
    def full_slug(self):
        return f"{self.project_slug}/{self.slug}"


class Checker:
    def __init__(self, *, url, record, http):
        self._base_url = url
        self._record = record
        self._http = http

    def check(self, project, repo):
        if not within_business_hours(datetime.now()):
            logger.info("skipping check: outside of business hours")
            return []
        repo = Repo(self._base_url, project, repo, record=self._record, http=self._http)
        return repo.alerts()


class JsonRecord:
    def __init__(self, *, database):
        self._db_path = Path(database)

    def record_alert(self, pr_id):
        db = self._read_db()
        db[pr_id] = datetime.now().isoformat()
        self._db_path.write_text(json.dumps(db))

    def alerted_recently(self, pr_id):
        db = self._read_db()
        if pr_id not in db:
            return False
        return datetime.now() - datetime.fromisoformat(db[pr_id]) < timedelta(hours=3)

    def _read_db(self):
        try:
            return json.loads(self._db_path.read_text())
        except FileNotFoundError:
            return {}


def check(url, repos, *, reporter, config=Config()):
    http = HttpClient(verify_https=config.verify_https)
    record = JsonRecord(database=config.database)
    checker = Checker(url=url, record=record, http=http)
    alerts = []
    exception = None
    for repo in repos:
        logger.info(f"checking repo: {repo}")
        project_slug, repo_slug = repo.split("/")
        try:
            alerts.extend(checker.check(project_slug, repo_slug))
        except FailedToGetData as exc:
            exception = exc
    reporter.report(alerts)
    if exception:
        raise exception
