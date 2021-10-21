# Git GPG Validator
Verify that the GPG key is valid on the GitHub account

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
- pipenv 2018.11.26

### Running

1. Installing Packages
```sh
pipenv install
```

2. Validate
```sh
pipenv run python3 verify.py
```

### [Simple Fingerprint Compare](./verify.py)

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
