# -*- coding: utf-8 -*-

import argparse
import os

from colorama import init, Fore, Style

from .clients import GitHub, GitLab
from .mapping import get_mapping
from .utils import err

init()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")


def get_parser():
    parser = argparse.ArgumentParser(
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


def main(args=None):
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
