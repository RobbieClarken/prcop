import requests


def check(base_url, project, repo):
    url = f"{base_url}/rest/api/1.0/projects/{project}/repos/{repo}/pull-requests"
    response = requests.get(url)
    alerts = []
    for pr in response.json()["values"]:
        approvals = sum(review["status"] == "APPROVED" for review in pr["reviewers"])
        if approvals < 2:
            alerts.append(f"{project}/{repo} needs reviews")
    return alerts
