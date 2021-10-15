# Git GPG Validator
Verify that the GPG key is valid on the GitHub account

## Before Starting

We can use a [GPG Key](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key) to verify the editor of the commit.

Authentication of the commit can protect projects and also help version tracing.

## Why this project?

I usually have two different git accounts(emails) working on GitHub and GitLab, both of them have different GPG keys.

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
