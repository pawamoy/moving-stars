# Moving Stars

:star: Copy your stars :star2: from one Git provider to another :stars:

![screenshot](screenshot.png)

Currently only support copying stars from GitHub to GitLab. Namespace and project name must be the same on GitHub and GitLab. Case is insensitive, though :+1:!

## Bash
Dependencies: `requests` and `colorama` (`pip install requests colorama`)

```bash
export GITHUB_TOKEN=<github_token>
export GITLAB_TOKEN=<gitlab_token>

python copy_stars.py
```

## Docker
```bash
docker run -e GITHUB_TOKEN=<github_token> -e GITLAB_TOKEN=<gitlab_token> --rm pawamoy/moving-stars
```

## Tokens
- [Create a new GitHub token](https://github.com/settings/tokens/new) with `read:user` scope.
- [Create a new GitLab token](https://gitlab.com/profile/personal_access_tokens) with `api` scope.

## Input file
A file containing the list of starred repositories that you want to copy on GitLab.
The format of the input file is very simple.

```
namespace/repository
namespace2/repository2
...
```

Example:
```
microsoft/ghcrawler-cli
github/VisualStudio
Pawamoy/moving-stars
this-repo/does-not-exist
cryptsetup/cryptsetup
```

## Other options
```console
$ python copy_stars.py -h
usage: copy_stars.py [-h] [-f FROM_FILE] [--no-pre-skip]

Command line tool to copy GitHub stars to GitLab.

optional arguments:
  -h, --help            show this help message and exit
  -f FROM_FILE, --from-file FROM_FILE
                        Read star list from file.
  -o OUTPUT_SOURCE_LIST, --output-source-list OUTPUT_SOURCE_LIST
                        Output downloaded source list to file.
  --no-pre-skip         Don't download list from target to skip already
                        starred projects.
```

It can be useful to first download your starred list, update it manually
(to correct unmatching namespaces / project names),
and then star on GitLab with this list:

```bash
python copy_stars.py -o star_list
# edit file manually...
python copy_stars.py -f star_list
```
