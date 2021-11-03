from typing import Dict

import pytest

from validator.config import GPG_SIGN, GPG_VERIFY
from validator.sign_verify import sign_text

from .config import TEST_KEYS


@pytest.fixture
def import_keys(request):
    sign_key, verify_key = request.param
    if sign_key:
        with open(f"tests/sample_keys/{sign_key['file']}", "rb") as key_fh:
            GPG_SIGN.import_keys(key_fh.read())
    if verify_key:
        with open(f"tests/sample_keys/{verify_key['file']}", "rb") as key_fh:
            GPG_VERIFY.import_keys(key_fh.read())
    yield
    if sign_key:
        GPG_SIGN.delete_keys(sign_key["fingerprint"], secret=True, passphrase=sign_key["passphrase"])
        GPG_SIGN.delete_keys(sign_key["fingerprint"], secret=False, passphrase=sign_key["passphrase"])
    if verify_key:
        GPG_VERIFY.delete_keys(verify_key["fingerprint"], secret=True, passphrase=verify_key["passphrase"])
        GPG_VERIFY.delete_keys(verify_key["fingerprint"], secret=False, passphrase=verify_key["passphrase"])


@pytest.mark.parametrize(
    "import_keys, sign_key, success",
    [
        ([TEST_KEYS[0], {}], TEST_KEYS[0], True),
        ([TEST_KEYS[0], {}], TEST_KEYS[1], False),
        ([TEST_KEYS[1], {}], TEST_KEYS[1], True),
        ([TEST_KEYS[1], {}], TEST_KEYS[0], False),
    ],
    indirect=["import_keys"],
)
def test_sign_text(import_keys, sign_key, success):
    print(GPG_SIGN.list_keys())
    print(sign_key["fingerprint"])
    signature = sign_text(GPG_SIGN, "TEST STRING", sign_key["fingerprint"], sign_key["passphrase"])
    message = GPG_SIGN.verify(signature)
    if success:
        assert message.valid is True
        assert message.fingerprint == sign_key["fingerprint"]
    else:
        assert message.valid is False
        assert message.fingerprint is None
