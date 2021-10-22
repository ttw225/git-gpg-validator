from typing import List, Tuple

from loguru import logger
import gnupg

from utils import get_github_gpgs
from config import SIGN_KEYID, VERIFY_GPGHOME, PAYLOAD


def sign_text(gpg: gnupg.GPG, text: str, key_id: str) -> bytes:
    """Sign text

    Args:
        gpg (gnupg.GPG): GPG for sign
        text (str): target text
        key_id (str): sign key id

    Returns:
        bytes: signature
    """
    signed = gpg.sign(text, keyid=key_id)
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
    default_gpg: gnupg.GPG = gnupg.GPG()
    text_signature: bytes = sign_text(default_gpg, PAYLOAD, SIGN_KEYID)
    # Verify signature
    platform_key_pairs: List[Tuple[str, str]] = get_github_gpgs()
    verify_gpg: gnupg.GPG = gnupg.GPG(gnupghome=VERIFY_GPGHOME)
    if verify_signature(verify_gpg, text_signature, platform_key_pairs):
        logger.success("[GPG Sign] Verified Successfully")
    else:
        logger.error("[GPG Sign] Verification Failed")
