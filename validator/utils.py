import os
from typing import List, Optional, Tuple

import git
import requests
from loguru import logger

from .config import GITHUB_GPG_URI, GITHUB_HEADERS


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
        return str(git.Repo(os.getcwd()).config_reader().get_value("user", "signingkey"))
    except Exception as err:
        logger.warning(f"[Git Config] user signingkey error: {err}")
        return None
