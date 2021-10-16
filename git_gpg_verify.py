import json
import os

import requests
from loguru import logger
import gnupg
import git


GITHUB_USERNAME = "ttw225"
GITHUB_GPG_URI = f"https://api.github.com/users/{GITHUB_USERNAME}/gpg_keys"
GITHUB_HEADERS = {"Accept": "application/vnd.github.v3+json"}


def get_github_gpgs() -> list:
    """Get GitHub GPG Key IDs

    Returns:
        list: GPG Key IDs
    """
    logger.info(f"[Git Platform] Getting GPG Keys from user {GITHUB_USERNAME}")
    try:
        response: json = requests.get(GITHUB_GPG_URI, headers=GITHUB_HEADERS).json()
    except Exception as err:
        logger.error(err)
    key_ids = parse_github_response(response)
    return key_ids


def parse_github_response(response: json) -> list:
    """Parse GitHub API Response

    Args:
        response (json): response

    Returns:
        list: GPG IDs
    """
    key_ids: list = []
    for keys in response:
        if keys["can_sign"] and keys["can_certify"]:
            logger.info(f"[GitHub GPG] ID: {keys['key_id']}")
            key_ids.append(keys["key_id"])
    return key_ids


def get_local_gpgs():
    pass


def get_project_sign() -> str:
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
        platform_key_ids: list = get_github_gpgs()
        logger.debug(f"[Platform Valid Key IDs] {platform_key_ids}")
    except Exception as err:
        logger.error(err)
