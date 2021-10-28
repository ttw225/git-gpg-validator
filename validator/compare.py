from typing import List, Optional, Tuple

import gnupg
from loguru import logger

from .utils import get_github_gpgs, get_project_sign


def compare_key(local_key: str, platform_keys: List[Tuple[str, str]]) -> bool:
    """Compare Key with fingerprint

    Args:
        local_key (str): local GPG Key ID
        platform_keys (List[Tuple[str, str]]): Platform GPG Key IDs

    Returns:
        bool: Local key valid or not
    """
    gpg = gnupg.GPG()
    local_fingerprint: str = gpg.import_keys(gpg.export_keys(local_key)).fingerprints[0]
    logger.debug(f"[Local Fingerprint] {local_fingerprint}")
    for keyid, pubkey in platform_keys:
        if local_fingerprint == gpg.import_keys(pubkey).fingerprints[0]:
            logger.debug(f"[Key Valid] ID: {keyid}")
            return True
    return False


if __name__ == "__main__":
    try:
        # Project GPG Key in Git Config (Local > Global)
        project_key_id: Optional[str] = get_project_sign()
        logger.debug(f"[Project Key ID] {project_key_id}")
        if not project_key_id:
            raise Exception("No Local GPG Key Setting")
        # Platform GPG Key(s)
        platform_key_pairs: List[Tuple[str, str]] = get_github_gpgs()
        if not platform_key_pairs:
            raise Exception("No Platform GPG Key Available")
        # Fingerprint Verification
        if compare_key(project_key_id, platform_key_pairs):
            logger.success("[GPG Key] Verified Successfully")
        else:
            logger.error("[GPG Key] Verification Failed")
    except Exception as err:
        logger.error(err)
