import pytest

from validator.config import GPG_SIGN, GPG_VERIFY


@pytest.fixture
def import_keys(request):
    sign_key, verify_key = request.param
    if sign_key:
        with open(f"tests/sample_keys/{sign_key['secret']}", "rb") as key_fh:
            GPG_SIGN.import_keys(key_fh.read(), passphrase=sign_key["passphrase"])
    if verify_key:
        with open(f"tests/sample_keys/{verify_key['public']}", "rb") as key_fh:
            GPG_VERIFY.import_keys(key_fh.read())
    yield
    if sign_key:
        GPG_SIGN.delete_keys(sign_key["fingerprint"], secret=True, passphrase=sign_key["passphrase"])
        GPG_SIGN.delete_keys(sign_key["fingerprint"], secret=False, passphrase=sign_key["passphrase"])
    if verify_key:
        GPG_VERIFY.delete_keys(verify_key["fingerprint"], secret=False)
