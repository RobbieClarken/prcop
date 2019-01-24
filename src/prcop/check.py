import requests


def check(base_url, project, repo):
    url = f"{base_url}/rest/api/1.0/projects/{project}/repos/{repo}/pull-requests"
    response = requests.get(url)
    approvals = sum(
        1 if review["status"] == "APPROVED" else 0
        for review in response.json()["values"][0]["reviewers"]
    )
    if approvals < 2:
        return [f"{project}/{repo} needs reviews"]
    else:
        return []
