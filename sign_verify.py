import gnupg

from loguru import logger

KET_ID = "68A8DC40153D6B6F"
PHRASE = "Have a nice day!"


def sign_text(text: str) -> bytes:
    """Sign text

    Args:
        text (str): target text

    Returns:
        bytes: signature
    """
    gpg = gnupg.GPG()
    signed = gpg.sign(PHRASE, keyid=KET_ID)
    logger.info(signed.data)
    return signed.data


if __name__ == "__main__":
    text_signature: bytes = sign_text(PHRASE)
