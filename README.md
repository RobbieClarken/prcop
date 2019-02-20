# prcop

Send Slack alerts to remind your team when reviews are overdue on pull requests.

Currently supports self-hosted Bitbucket servers.

## Installation

```
python3.7 -m pip install prcop
```

## Usage

```
prcop run \
  --bitbucket-url https://bitbucket.example.com/ \
  --slack-webhook https://hooks.slack.com/services/<id> \
  --slack-channel development \
  project1/repo1 project1/repo2 project2/repo3
```
