# Moving Stars

:star: Copy your stars :star2: from one Git provider to another :stars:

Currently only support copying stars from GitHub to GitLab.

## Bash

Dependencies: `requests` (`pip install requests`)

```bash
export GITHUB_TOKEN=<github_token>
export GITLAB_TOKEN=<gitlab_token>

python copy_stars.py  # [-f INPUT_FILE]
```

## Docker

```bash
docker run -e GITHUB_TOKEN=<github_token> -e GITLAB_TOKEN=<gitlab_token> --rm pawamoy/moving-stars
```

## Tokens

- [Create a new GitHub token](https://github.com/settings/tokens/new) with `read:user` scope.
- [Create a new GitLab token](https://gitlab.com/profile/personal_access_tokens) with `api` scope.
