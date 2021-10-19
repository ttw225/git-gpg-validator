from typing import List, Tuple

from loguru import logger
import gnupg

from verify import get_github_gpgs

SIGN_KEYID = "68A8DC40153D6B6F"
PAYLOAD = "Have a nice day!"
GNUPGHOME = ".gpg_folder"


def sign_text(text: str) -> bytes:
    """Sign text

    Args:
        text (str): target text

    Returns:
        bytes: signature
    """
    gpg = gnupg.GPG()
    signed = gpg.sign(text, keyid=SIGN_KEYID)
    return signed.data


def verify_signature(signature: bytes) -> bool:
    """Verify Message using Platform GPG Keys

    Args:
        signature (bytes): Message Signed with specific GPG Key

    Returns:
        bool: Valid or not
    """
    platform_key_pairs: List[Tuple[str, str]] = get_github_gpgs()
    # Import Platform GPG Keys
    gpg = gnupg.GPG(gnupghome=GNUPGHOME)
    for _, pubkey in platform_key_pairs:
        gpg.import_keys(pubkey)
    return gpg.verify(signature).valid


if __name__ == "__main__":
    text_signature: bytes = sign_text(PAYLOAD)
    if verify_signature(text_signature):
        logger.success("[GPG Sign] Verified Successfully")
    else:
        logger.error("[GPG Sign] Verification Failed")
