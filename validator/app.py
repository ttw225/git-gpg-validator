import argparse
from typing import List, Optional, Tuple

from loguru import logger

from .compare import compare_key
from .config import GPG_SIGN, GPG_VERIFY, PAYLOAD
from .sign_verify import sign_text, verify_signature
from .utils import get_github_gpgs, get_project_sign


def main(args: argparse.Namespace) -> bool:
    """GPG Key Validator

    Args:
        args (argparse.Namespace): arguments

    Raises:
        Exception: Local GPG Error
        Exception: Platform GPG Error

    Returns:
        bool: Valid or not
    """
    project_key_id: str = ""
    if args.key:
        # User-specified GPG Key
        project_key_id = args.key
    else:
        # Project GPG Key Setting
        key_id: Optional[str] = get_project_sign()
        if key_id:
            project_key_id = key_id
        else:
            raise Exception("No Local GPG Key Setting")
    # Check Key Available
    logger.debug(f"[Project Key ID] {project_key_id}")
    pub_key: str = GPG_SIGN.export_keys(project_key_id)
    if not project_key_id or not pub_key:
        raise Exception("No Local GPG Key")
    # Platform GPG Key(s)
    platform_key_pairs: List[Tuple[str, str]] = get_github_gpgs()
    if not platform_key_pairs:
        raise Exception("No Platform GPG Key Available")
    if args.method == "simple":
        # Compare Fingerprint
        # Fingerprint Verification
        if compare_key(project_key_id, platform_key_pairs):
            logger.success("[GPG Simple] Verified Successfully")
            return True
        logger.error("[GPG Simple] Verification Failed")
    else:
        # Sign text
        text_signature: bytes = sign_text(GPG_SIGN, PAYLOAD, project_key_id)
        # Verify signature
        if verify_signature(GPG_VERIFY, text_signature, platform_key_pairs):
            logger.success("[GPG Hard] Verified Successfully")
            return True
        logger.error("[GPG Hard] Verification Failed")
    return False


if __name__ == "__main__":
    PARSER: argparse.ArgumentParser = argparse.ArgumentParser(description="GPG Key Validator")
    PARSER.add_argument(
        "-m",
        "--method",
        type=str,
        choices=["simple", "hard"],
        default="simple",
        help="simple: compare fingerprint; hard: sign and verify",
    )
    PARSER.add_argument("-k", "--key", type=str, help="Use default key or set a Key ID for signing")
    ARGS: argparse.Namespace = PARSER.parse_args()
    main(ARGS)
