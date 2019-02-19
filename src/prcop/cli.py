import click

from .checker import check
from .config import Config
from .reporters import SlackReporter


@click.group()
def cli():
    pass


@cli.command()
@click.option("--bitbucket-url", required=True)
@click.option("--slack-webhook", required=True)
@click.option("--slack-channel", required=True)
@click.option("--database")
@click.option("--no-verify-https", is_flag=True)
@click.argument("repos", nargs=-1, metavar="[REPO...]")
def run(bitbucket_url, slack_webhook, slack_channel, repos, database, no_verify_https):
    config = Config(verify_https=not no_verify_https)
    if database:
        config.database = database
    reporter = SlackReporter(url=slack_webhook, channel=slack_channel)
    check(bitbucket_url, list(repos), reporter=reporter, config=config)
