import os
from typing import Dict

import gnupg
from dotenv import load_dotenv

load_dotenv()

# GPG Setting
SIGN_KEYID: str = os.environ.get("SIGN_KEYID", "")
PAYLOAD: str = "Try a little harder to be a little better"
SIGN_GPGHOME: str = os.environ.get("SIGN_GPGHOME", ".gpg_sign")
VERIFY_GPGHOME: str = os.environ.get("VERIFY_GPGHOME", ".gpg_verify")

# GPG Object
GPG_SIGN: gnupg.GPG = gnupg.GPG(gnupghome=SIGN_GPGHOME)
GPG_VERIFY: gnupg.GPG = gnupg.GPG(gnupghome=VERIFY_GPGHOME)

# Git Platform
GITHUB_USERNAME: str = os.environ.get("GITHUB_USERNAME", "")
GITHUB_GPG_URI: str = f"https://api.github.com/users/{GITHUB_USERNAME}/gpg_keys"
GITHUB_HEADERS: Dict[str, str] = {"Accept": "application/vnd.github.v3+json"}
