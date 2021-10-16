import json
import os
from typing import List, Tuple

import requests
from loguru import logger
import gnupg
import git


GITHUB_USERNAME = "ttw225"
GITHUB_GPG_URI = f"https://api.github.com/users/{GITHUB_USERNAME}/gpg_keys"
GITHUB_HEADERS = {"Accept": "application/vnd.github.v3+json"}


def get_github_gpgs() -> List[Tuple[str, str]]:
    """Get GitHub GPG Key IDs

    Returns:
        List[Tuple[str, str]]: Pair of GPG ID and Public Key
    """
    logger.info(f"[Git Platform] Getting GPG Keys from user {GITHUB_USERNAME}")
    try:
        response: json = requests.get(GITHUB_GPG_URI, headers=GITHUB_HEADERS).json()
    except Exception as err:
        logger.error(err)
    key_ids = parse_github_response(response)
    return key_ids


def parse_github_response(response: json) -> List[Tuple[str, str]]:
    """Parse GitHub API Response

    Args:
        response (json): response

    Returns:
        List[Tuple[str, str]]: Pair of GPG ID and Public Key
    """
    gpg_keys: List[Tuple[str, str]] = []
    for keys in response:
        if keys["can_sign"] and keys["can_certify"]:
            logger.info(f"[GitHub GPG] ID: {keys['key_id']}")
            gpg_keys.append((keys["key_id"], keys["raw_key"]))
    return gpg_keys


def get_local_gpg_pub(gpg_id: str) -> str:
    """Get Local GPG Public Key

    Args:
        gpg_id (str): GPG Key ID

    Returns:
        str: Public Key
    """
    gpg = gnupg.GPG()
    gpg_key = gpg.export_keys(gpg_id)
    return gpg_key


def get_project_sign() -> str:
    """Get Local Git user.signingkey Setting

    Returns:
        str: user.signingkey
    """
    logger.info("[Git Config] Getting user signingkey settings")
    try:
        return git.Repo(os.getcwd()).config_reader().get_value("user", "signingkey")
    except Exception as err:
        logger.warning(f"[Git Conofig] user signingkey error: {err}")
        return None


if __name__ == "__main__":
    try:
        project_key_id: str = get_project_sign()
        logger.debug(f"[Project Key ID] {project_key_id}")
        if not project_key_id:
            raise Exception("No Local GPG Key Setting")
        local_gpg_pub: str = get_local_gpg_pub(project_key_id)
        if not local_gpg_pub:
            raise Exception("Local GPG Key Not Found")
        platform_keys: List[Tuple[str, str]] = get_github_gpgs()
        if not platform_keys:
            raise Exception("No Platform GPG Key Available")
    except Exception as err:
        logger.error(err)
