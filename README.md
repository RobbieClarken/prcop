# prcop

[![Build Status](https://travis-ci.org/RobbieClarken/prcop.svg?branch=master)](https://travis-ci.org/RobbieClarken/prcop)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/RobbieClarken/prcop/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


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
