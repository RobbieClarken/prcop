import json
from datetime import datetime, timedelta
from pathlib import Path

from .business_hours import business_hours_between_dates, within_business_hours
from .config import Config
from .http_client import HttpClient


class PullRequest:

    _MIN_TIME_OPENED = timedelta(hours=3)
    _MIN_APPROVALS = 2

    def __init__(self, data, *, repo, record):
        self._data = data
        self._repo = repo
        self._record = record

    def alerts(self):
        if (
            self._business_hours_since_opened >= self._MIN_TIME_OPENED
            and not self._recently_alerted
            and self._approvals < self._MIN_APPROVALS
            and not self._needs_work
        ):
            self._record.record_alert(self._id)
            return [self._alert_message]
        return []

    @property
    def _id(self):
        return str(self._data["id"])

    @property
    def _title(self):
        return self._data["title"]

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
    def _business_hours_since_opened(self):
        return business_hours_between_dates(
            datetime.fromtimestamp(self._data["createdDate"] / 1000), datetime.now()
        )

    @property
    def _alert_message(self):
        return f'{self._repo.project_slug}/{self._repo.slug} PR: "{self._title}" needs reviews'


class Repo:
    def __init__(self, base_url, project, repo, *, record, http):
        self._base_url = base_url
        self.project_slug = project
        self.slug = repo
        self._record = record
        self._http = http

    def alerts(self):
        url = (
            f"{self._base_url}/rest/api/1.0/projects/{self.project_slug}"
            f"/repos/{self.slug}/pull-requests"
        )
        api_response = self._http.get(url)
        alerts = []
        for pr_data in api_response["values"]:
            pr = PullRequest(pr_data, repo=self, record=self._record)
            alerts += pr.alerts()
        return alerts


class Checker:
    def __init__(self, *, url, record, http):
        self._base_url = url
        self._record = record
        self._http = http

    def check(self, project, repo):
        if not within_business_hours(datetime.now()):
            return []
        repo = Repo(self._base_url, project, repo, record=self._record, http=self._http)
        return repo.alerts()


class JsonRecord:
    _db_path = Path("/tmp/prcopdb.json")

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


def check(url, repos, *, config=Config()):
    http = HttpClient(config)
    checker = Checker(url=url, record=JsonRecord(), http=http)
    alerts = []
    for repo in repos:
        project_key, repo_key = repo.split("/")
        alerts.extend(checker.check(project_key, repo_key))
    return alerts
