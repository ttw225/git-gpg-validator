import os

import git
import pytest

from validator.config import GPG_SIGN
from validator.utils import get_project_sign


@pytest.fixture
def import_sign_keys(key_files=["example_private.pgp", "example2_private.pgp"]):
    for key_file in key_files:
        with open(f"tests/sample_keys/{key_file}", "rb") as key_fh:
            GPG_SIGN.import_keys(key_fh.read())


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
