import os

from dotenv import load_dotenv

load_dotenv()

# Sign and Verify
SIGN_KEYID = os.environ.get("SIGN_KEYID", "")
VERIFY_GPGHOME = os.environ.get("VERIFY_GPGHOME", ".gpg_folder")
