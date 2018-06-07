Moving Stars
============

Copy your stars from one Git provider to another.

Currently only support moving stars from GitHub to GitLab.

```bash
export GITHUB_TOKEN=<github_token>
export GITLAB_TOKEN=<gitlab_token>

python move_stars.py  # [-f INPUT_FILE]
```

Or with Docker:

```bash
docker run -e GITHUB_TOKEN=<github_token> -e GITLAB_TOKEN=<gitlab_token> --rm pawamoy/moving-stars
```

- [Create a new GitHub token](https://github.com/settings/tokens/new) with `read:user` scope.
- [Create a new GitLab token](https://gitlab.com/profile/personal_access_tokens) with `api` scope.

