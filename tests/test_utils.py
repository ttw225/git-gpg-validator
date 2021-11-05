import os
from typing import List

import git
import pytest

from validator.config import GPG_SIGN
from validator.utils import get_project_sign, parse_github_response

from .config import TEST_KEYS


@pytest.fixture
def backup_git_key():
    original_key: str = str(git.Repo(os.getcwd()).config_reader().get_value("user", "signingkey"))
    # Set to empty
    git.Repo(os.getcwd()).config_writer().set_value("user", "signingkey", "").release()
    yield
    # Restore
    git.Repo(os.getcwd()).config_writer().set_value("user", "signingkey", original_key).release()


@pytest.mark.parametrize("key_id", [(""), ("4BDCFAF35C34FA95"), ("32C5B310A13AFADA")])
def test_get_project_sign(backup_git_key, key_id: str):
    git.Repo(os.getcwd()).config_writer().set_value("user", "signingkey", key_id).release()
    assert get_project_sign() == key_id


@pytest.mark.parametrize(
    "response, output",
    [
        ([], []),
        (
            [
                {
                    "key_id": "KEY-ID-OK",
                    "raw_key": "RAW-KEY-OK",
                    "can_certify": True,
                }
            ],
            [("KEY-ID-OK", "RAW-KEY-OK")],
        ),
        (
            [
                {
                    "key_id": "KEY-ID-OK",
                    "raw_key": "RAW-KEY-OK",
                    "can_certify": True,
                },
                {
                    "key_id": "KEY-ID-BAD",
                    "raw_key": "RAW-KEY-BAD",
                    "can_certify": False,
                },
            ],
            [("KEY-ID-OK", "RAW-KEY-OK")],
        ),
        (
            [
                {
                    "key_id": "KEY-ID-OK",
                    "raw_key": "RAW-KEY-OK",
                    "can_certify": True,
                },
                {
                    "key_id": "KEY-ID-OK1",
                    "raw_key": "RAW-KEY-OK1",
                    "can_certify": True,
                },
                {
                    "key_id": "KEY-ID-BAD",
                    "raw_key": "RAW-KEY-BAD",
                    "can_certify": False,
                },
            ],
            [("KEY-ID-OK", "RAW-KEY-OK"), ("KEY-ID-OK1", "RAW-KEY-OK1")],
        ),
    ],
)
def test_parse_github_response(response, output):
    assert parse_github_response(response) == output
