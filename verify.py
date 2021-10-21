import os
from typing import List, Tuple, Optional

import requests
from loguru import logger
import gnupg
import git

from config import GITHUB_GPG_URI, GITHUB_HEADERS


def get_github_gpgs() -> List[Tuple[str, str]]:
    """Get GitHub GPG Key Pairs (ID, Pubkey)

    Returns:
        List[Tuple[str, str]]: Pair of GPG ID and Public Key
    """
    try:
        response: list = requests.get(GITHUB_GPG_URI, headers=GITHUB_HEADERS).json()
    except Exception as err:
        logger.error(err)
    key_ids = parse_github_response(response)
    return key_ids


def parse_github_response(response: list) -> List[Tuple[str, str]]:
    """Parse GitHub API Response

    Args:
        response (list): response

    Returns:
        List[Tuple[str, str]]: Pair of GPG ID and Public Key
    """
    gpg_keys: List[Tuple[str, str]] = []
    for keys in response:
        if keys["can_sign"] and keys["can_certify"]:
            logger.info(f"[GitHub GPG] ID: {keys['key_id']}")
            gpg_keys.append((keys["key_id"], keys["raw_key"]))
    return gpg_keys


def get_project_sign() -> Optional[str]:
    """Get Local Git user.signingkey Setting

    Returns:
        str: user.signingkey
    """
    logger.info("[Git Config] Getting user signingkey settings")
    try:
        return git.Repo(os.getcwd()).config_reader().get_value("user", "signingkey")
    except Exception as err:
        logger.warning(f"[Git Config] user signingkey error: {err}")
        return None


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
