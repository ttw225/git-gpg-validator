import pytest

from validator.config import GPG_SIGN
from validator.utils import get_project_sign


@pytest.fixture
def import_sign_keys(key_files=["example_private.pgp", "example2_private.pgp"]):
    for key_file in key_files:
        with open(f"tests/sample_keys/{key_file}", "rb") as key_fh:
            GPG_SIGN.import_keys(key_fh.read())


def test_get_project_sign():
    assert get_project_sign() == "68A8DC40153D6B6F"
