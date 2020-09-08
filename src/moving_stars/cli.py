# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m moving_stars` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `moving_stars.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `moving_stars.__main__` in `sys.modules`.

"""Module that contains the command line application."""

import argparse
import os
from typing import List, Optional

from colorama import init, Fore, Style

from moving_stars.clients import GitHub, GitLab
from moving_stars.mapping import get_mapping
from moving_stars.utils import err

init()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")


def get_parser() -> argparse.ArgumentParser:
    """
    Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(
        prog="moving-stars",
        description="Command line tool to copy GitHub stars to GitLab."
    )
    mxg = parser.add_mutually_exclusive_group(required=False)
    mxg.add_argument(
        "-f",
        "--from-file",
        action="store",
        dest="from_file",
        default=None,
        help="Read star list from file.",
    )
    mxg.add_argument(
        "-o",
        "--output-source-list",
        action="store",
        dest="output_source_list",
        default=None,
        help="Output downloaded source list to file.",
    )
    parser.add_argument(
        "--no-pre-skip",
        action="store_true",
        dest="no_pre_skip",
        default=False,
        help="Don't download list from target to skip already starred projects.",
    )
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Run the main program.

    This function is executed when you type `moving-stars` or `python -m moving_stars`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    args = parser.parse_args(args=args)

    if args.from_file is None:
        if not GITHUB_TOKEN:
            err(Style.RESET_ALL + "GITHUB_TOKEN environment variable must be set")
            return 1

        github = GitHub(GITHUB_TOKEN)
        github_star_list = github.get_stars()

        if args.output_source_list:
            with open(args.output_source_list, "w") as stream:
                for star in github_star_list:
                    stream.write(star + "\n")
            return 0

    else:
        with open(args.from_file) as stream:
            github_star_list = {line.rstrip("\n") for line in stream.readlines()} - {""}
        err(
            Style.RESET_ALL
            + Style.BRIGHT
            + "Read a list of %d starred repositories" % len(github_star_list)
        )

    if not GITLAB_TOKEN:
        err(Style.RESET_ALL + "GITLAB_TOKEN environment variable must be set")
        return 1

    gitlab = GitLab(GITLAB_TOKEN)

    if not args.no_pre_skip:
        gitlab_star_list = gitlab.get_stars()

        github_set = set(star.lower() for star in github_star_list)
        gitlab_set = set(star.lower() for star in gitlab_star_list)

        stars_to_sync = github_set - gitlab_set

        skipped = len(github_set) - len(stars_to_sync)
        if skipped > 0:
            err(
                Style.RESET_ALL
                + Fore.YELLOW
                + "Skipping %d repositories that are already starred on GitLab"
                % skipped
            )

    else:
        skipped = 0
        stars_to_sync = github_star_list

    # update namespace/project with mapping
    mapping = get_mapping()
    mapped_stars_to_sync = list()
    for star in stars_to_sync:
        github_star = 'github.com:' + star
        if github_star in mapping:
            mapped_stars_to_sync.append(mapping[github_star]['gitlab.com'])
        else:
            mapped_stars_to_sync.append(star)
    mapped_stars_to_sync = list(sorted(mapped_stars_to_sync))

    report = gitlab.post_stars(mapped_stars_to_sync)

    err(Style.RESET_ALL + Style.BRIGHT)
    err("---------- Report ----------")
    err("")
    err("Stars:     %d" % report["success"])
    err("Skipped:   %d" % (report["skip"] + skipped))
    err("Not found: %d" % report["not_found"])
    err("Errors:    %d" % report["error"])

    return 0
