from typing import List, Tuple

import gnupg
from loguru import logger

from .config import GPG_SIGN, GPG_VERIFY, PAYLOAD, SIGN_KEYID
from .utils import get_github_gpgs


def sign_text(gpg: gnupg.GPG, text: str, key_id: str) -> bytes:
    """Sign text

    Args:
        gpg (gnupg.GPG): GPG for sign
        text (str): target text
        key_id (str): sign key id

    Returns:
        bytes: signature
    """
    # use `-u` to specific the sign key, without using default key-ring
    signed = gpg.sign(text, keyid=key_id, extra_args=["-u", key_id])
    return signed.data


def verify_signature(gpg: gnupg.GPG, signature: bytes, key_pairs: List[Tuple[str, str]]) -> bool:
    """Verify Message using Platform GPG Keys

    Args:
        gpg (gnupg.GPG): GPG for verify
        signature (bytes): Message Signed with specific GPG Key
        key_pairs (List[Tuple[str, str]]): Platform GPG key-paris

    Returns:
        bool: Valid or not
    """
    # Import Platform GPG Keys
    for _, pubkey in key_pairs:
        gpg.import_keys(pubkey)
    return gpg.verify(signature).valid


if __name__ == "__main__":
    # Use the Key with the specified ID for signing
    text_signature: bytes = sign_text(GPG_SIGN, PAYLOAD, SIGN_KEYID)
    # Verify signature
    platform_key_pairs: List[Tuple[str, str]] = get_github_gpgs()
    if verify_signature(GPG_VERIFY, text_signature, platform_key_pairs):
        logger.success("[GPG Sign] Verified Successfully")
    else:
        logger.error("[GPG Sign] Verification Failed")
