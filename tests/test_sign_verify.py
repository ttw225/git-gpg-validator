from typing import Dict

import pytest

from validator.config import GPG_SIGN, GPG_VERIFY
from validator.sign_verify import sign_text, verify_signature

from .config import TEST_KEYS


@pytest.mark.parametrize(
    "import_keys, sign_key, success",
    [
        ([TEST_KEYS[0], {}], TEST_KEYS[0], True),
        ([TEST_KEYS[0], {}], TEST_KEYS[1], False),
        ([TEST_KEYS[1], {}], TEST_KEYS[0], False),
        ([TEST_KEYS[1], {}], TEST_KEYS[1], True),
    ],
    indirect=["import_keys"],
)
def test_sign_text(import_keys, sign_key, success):
    signature = sign_text(GPG_SIGN, "TEST STRING", sign_key["id"])
    message = GPG_SIGN.verify(signature)
    if success:
        assert message.valid is True
        assert message.fingerprint == sign_key["fingerprint"]
    else:
        assert message.valid is False
        assert message.fingerprint is None


@pytest.mark.parametrize(
    "import_keys, sign_key, verify_key",
    [
        ([TEST_KEYS[0], TEST_KEYS[0]], TEST_KEYS[0], TEST_KEYS[0]),
        ([TEST_KEYS[0], TEST_KEYS[1]], TEST_KEYS[0], TEST_KEYS[1]),
        ([TEST_KEYS[1], TEST_KEYS[0]], TEST_KEYS[1], TEST_KEYS[0]),
        ([TEST_KEYS[1], TEST_KEYS[1]], TEST_KEYS[1], TEST_KEYS[1]),
    ],
    indirect=["import_keys"],
)
def test_verify_signature(import_keys, sign_key, verify_key):
    signature = sign_text(GPG_SIGN, "TEST STRING", sign_key["id"])
    key_pairs = [(verify_key["id"], open(f"tests/sample_keys/{verify_key['public']}", "rb").read())]
    if sign_key == verify_key:
        assert verify_signature(GPG_VERIFY, signature, key_pairs) is True
    else:
        assert verify_signature(GPG_VERIFY, signature, key_pairs) is False
