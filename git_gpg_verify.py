import json

import requests
from loguru import logger


GITHUB_USERNAME = "ttw225"
GITHUB_GPG_URI = f"https://api.github.com/users/{GITHUB_USERNAME}/gpg_keys"
GITHUB_HEADERS = {"Accept": "application/vnd.github.v3+json"}


def get_github_gpgkeys() -> list:
    """Get GitHub GPG Key IDs

    Returns:
        list: GPG Key IDs
    """
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


if __name__ == "__main__":
    gpgkey_ids: list = get_github_gpgkeys()
    logger.info(f"[GitHub Valid IDs] {gpgkey_ids}")
