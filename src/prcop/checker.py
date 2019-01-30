import json
from datetime import datetime, timedelta
from pathlib import Path

import requests

from .business_hours import within_business_hours


class Checker:
    def __init__(self, *, record):
        self._record = record

    def check(self, base_url, project, repo):
        if not within_business_hours(datetime.now()):
            return []
        url = f"{base_url}/rest/api/1.0/projects/{project}/repos/{repo}/pull-requests"
        response = requests.get(url)
        alerts = []
        for pr in response.json()["values"]:
            pr_id = str(pr["id"])
            approvals = sum(review["status"] == "APPROVED" for review in pr["reviewers"])
            needs_work = any(review["status"] == "NEEDS_WORK" for review in pr["reviewers"])
            if not self._record.alerted_recently(pr_id) and approvals < 2 and not needs_work:
                title = pr["title"]
                alerts.append(f'{project}/{repo} PR: "{title}" needs reviews')
                self._record.record_alert(pr_id)
        return alerts


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


check = Checker(record=JsonRecord()).check
