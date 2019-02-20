import logging

import click

from .checker import check
from .config import Config
from .reporters import SlackReporter


logging.basicConfig(level="WARNING", format="%(asctime)s [%(levelname)s] %(name)s %(message)s")


@click.group()
def cli():
    pass


@cli.command()
@click.option("--bitbucket-url", required=True)
@click.option("--slack-webhook", required=True)
@click.option("--slack-channel", required=True)
@click.option("-i", "--input", "input_file", type=click.File("r"))
@click.option("--database")
@click.option("--no-verify-https", is_flag=True)
@click.option("-v", "--verbose", count=True)
@click.argument("repos", nargs=-1, metavar="[REPO...]")
def run(
    bitbucket_url,
    slack_webhook,
    slack_channel,
    input_file,
    database,
    no_verify_https,
    verbose,
    repos,
):
    if verbose:
        logging.getLogger().setLevel("DEBUG" if verbose > 1 else "INFO")
    repos = list(repos)
    if input_file:
        repos.extend(l.strip() for l in input_file.readlines())
    config = Config(verify_https=not no_verify_https)
    if database:
        config.database = database
    reporter = SlackReporter(url=slack_webhook, channel=slack_channel)
    check(bitbucket_url, repos, reporter=reporter, config=config)
