from pathlib import Path
from tempfile import TemporaryDirectory

import freezegun
import requests_mock
from behave import fixture, use_fixture

from prcop.config import Config


@fixture
def prcop_config_fixture(context):
    with TemporaryDirectory() as tmp_dir:
        database = str(Path(tmp_dir) / "prcop.json")
        context.prcop_config = Config(database=database)
        yield


@fixture
def request_mock_fixture(context):
    with requests_mock.Mocker() as m:
        context.requests_mock = m
        yield


@fixture
def freezegun_fixture(context):
    with freezegun.freeze_time("2019-02-04 16:00") as frozen_datetime:
        context.frozen_datetime = frozen_datetime
        yield


def before_scenario(context, scenario):
    use_fixture(prcop_config_fixture, context)
    for tag in scenario.feature.tags:
        if tag == "fixture.requests_mock":
            use_fixture(request_mock_fixture, context)
        elif tag == "fixture.freezegun":
            use_fixture(freezegun_fixture, context)
        else:
            raise NotImplementedError(f"{tag} is not implemented")
