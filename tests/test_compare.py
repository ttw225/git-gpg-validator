import pytest

from validator.compare import compare_key

from .config import TEST_KEYS


@pytest.mark.parametrize(
    "import_keys, sign_key, verify_key",
    [
        ([TEST_KEYS[0], {}], TEST_KEYS[0], TEST_KEYS[0]),
        ([TEST_KEYS[0], {}], TEST_KEYS[0], TEST_KEYS[1]),
        ([TEST_KEYS[1], {}], TEST_KEYS[1], TEST_KEYS[0]),
        ([TEST_KEYS[1], {}], TEST_KEYS[1], TEST_KEYS[1]),
    ],
    indirect=["import_keys"],
)
def test_sign_text(import_keys, sign_key, verify_key):
    key_pairs = [(verify_key["id"], open(f"tests/sample_keys/{verify_key['public']}", "rb").read())]
    if sign_key == verify_key:
        assert compare_key(sign_key["id"], key_pairs) == True
    else:
        assert compare_key(sign_key["id"], key_pairs) == False
