# Git GPG Validator
Verify that the GPG key is valid on the GitHub account

[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Ochrona](https://img.shields.io/badge/secured_by-ochrona-blue)](https://ochrona.dev)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## Before Starting

We can use a [GPG Key](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key) to verify the editor of the commit.

Authentication of the commit can protect projects and also help version tracing.

## Why this project?

People usually have different git accounts(emails) working on GitHub, GitLab, etc., both of them have different GPG keys.

To sign the commit correctly, it is better to verify the GPG key between the local settings and the git platform settings before uploading.

## Tools
### GPG Command
[GnuGPG](https://gnupg.org/)

[GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key)

+ List local GPG Keys
    ```sh
    gpg --list-secret-keys --keyid-format=long
    ```

### GitHub API
[GitHub API Docs](https://docs.github.com/en/rest/reference)

+ [Get User GPG Keys Doc](https://docs.github.com/en/rest/reference/users#list-gpg-keys-for-a-user)
    ```sh
    curl \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/users/USERNAME/gpg_keys
    ```

### Git Command
Show git log with signatures
```sh
git log --show-signature
```

## Validator

## Getting Started

### Prerequisites

- python 3.7
- pipenv 2021.5.29

### Running

1. Installing Packages
```sh
pipenv install
```

2. Validate
```sh
pipenv run python3 validator/app.py
```

Help
```sh
pipenv run python3 validator/app.py --help
```
```sh
usage: app.py [-h] [-m {simple,hard}] [-k KEY]

GPG Key Validator

optional arguments:
  -h, --help            show this help message and exit
  -m {simple,hard}, --method {simple,hard}
                        simple: compare fingerprint; hard: sign and verify
  -k KEY, --key KEY     Use default key or set a Key ID for signing
```

Example:
```sh
# Enter virtual environment
pipenv shell

# Simple Verify
## Use project default key, and compare fingerprint only
python3 validator/app.py

## Use specific key, and compare fingerprint only
python3 validator/app.py -k "KEY_ID"

# Hard Verify
mkdir .gpg_folder

## Use project default key, and do a sign-verify check
python3 validator/app.py -m hard

## Use specific key, and a sign-verify check
python3 validator/app.py -m hard -k "KEY_ID"
```

### [Simple Fingerprint Compare](./compare.py)

Applicable to the situation where the same key is used for encryption and decryption.

This script will compare GPG Key fingerprint between git config setting and platform settings.

> The fingerprint is derived from the public key and creation timestamp -- both are contained in the public keys listed on the site. [reference](https://stackoverflow.com/a/46916593)

### [Hard Verify](./sign_verify.py)

Some developers separate the keys for signing and verification. At this time, the actual signing and verification can confirm whether the key is set correctly.

Verification flow:

1. Sign text: use project default key or specific key to sign text
2. Import platform GPG keys
    The `verify_signature` function will import platform's key into temporary GPG folder (default is `.gpg_folder`).
3. Use temporary GPG object to verify the signature from step 1.
