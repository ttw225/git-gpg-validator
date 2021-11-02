import os
from typing import List

import git
import pytest

from validator.config import GPG_SIGN
from validator.utils import get_project_sign


TEST_KEYS = [
    {
        "file": "example_private.pgp",
        "fingerprint": "7D210A94B74DD63A4C3C64254BDCFAF35C34FA95",
        "passphrase": "very example p@ssword",
    },
    {
        "file": "example2_private.pgp",
        "fingerprint": "25178EFFE362212489FDA16F32C5B310A13AFADA",
        "passphrase": "very example2 p@ssw0rd",
    },
]


@pytest.fixture
def import_sign_keys(key_files=TEST_KEYS):
    for key_file in key_files:
        with open(f"tests/sample_keys/{key_file['file']}", "rb") as key_fh:
            GPG_SIGN.import_keys(key_fh.read())
    yield
    for key_file in key_files:
        GPG_SIGN.delete_keys(key_file["fingerprint"], secret=True, passphrase=key_file["passphrase"])
        GPG_SIGN.delete_keys(key_file["fingerprint"], secret=False, passphrase=key_file["passphrase"])


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


def test_import_sign(import_sign_keys):
    assert len(GPG_SIGN.list_keys()) == len(TEST_KEYS)
