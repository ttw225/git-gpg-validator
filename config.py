import os

from dotenv import load_dotenv

load_dotenv()

# Sign and Verify
SIGN_KEYID = os.environ.get("SIGN_KEYID", "")
VERIFY_GPGHOME = os.environ.get("VERIFY_GPGHOME", ".gpg_folder")

# Sign
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "")
GITHUB_GPG_URI = f"https://api.github.com/users/{GITHUB_USERNAME}/gpg_keys"
GITHUB_HEADERS = {"Accept": "application/vnd.github.v3+json"}
