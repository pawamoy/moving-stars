# Moving Stars

[![ci](https://github.com/pawamoy/moving-stars/workflows/ci/badge.svg)](https://github.com/pawamoy/moving-stars/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/moving-stars/)
[![pypi version](https://img.shields.io/pypi/v/moving-stars.svg)](https://pypi.org/project/moving-stars/)

:star: Star on GitLab.com the same repos your starred on GitHub.com! :stars:

![screenshot](screenshot.png)

Namespace and project name must be the same on GitHub and GitLab.
Case is insensitive though :+1:!

## Requirements

Moving Stars requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.8

# make it available globally
pyenv global system 3.6.8
```
</details>

## Installation

With `pip`:
```bash
python3.6 -m pip install moving-stars
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.6 -m pip install --user pipx

pipx install --python python3.6 moving-stars
```

## Usage

### Bash
```bash
export GITHUB_TOKEN=<github_token>
export GITLAB_TOKEN=<gitlab_token>

moving-stars
```

### Docker

```bash
docker run -e GITHUB_TOKEN=<github_token> -e GITLAB_TOKEN=<gitlab_token> --rm pawamoy/moving-stars
```

### Tokens

- [Create a new GitHub token](https://github.com/settings/tokens/new) with `read:user` scope.
- [Create a new GitLab token](https://gitlab.com/profile/personal_access_tokens) with `api` scope.

### Input file

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

### Other options

```console
$ moving-stars -h
usage: moving-stars [-h] [-f FROM_FILE] [--no-pre-skip]

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
moving-stars -o star_list
# edit file manually...
moving-stars -f star_list
```
