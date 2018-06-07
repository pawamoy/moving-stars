#!/usr/bin/env python

import argparse
import os
import requests
import sys

from colorama import init, Fore, Back, Style

init()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN', '')


def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Command line tool to copy GitHub stars to GitLab.')
    parser.add_argument(
        '-f', '--from-file', action='store', dest='from_file', default=None,
        help='Read star list from file.')
    parser.add_argument('--no-pre-skip', action='store_true',
        dest='no_pre_skip', default=False,
        help="Don't download list from target to skip already starred projects.")
    return parser


class Provider(object):
    name = 'Generic Provider'
    api_url = ''
    starred_request = ''
    path_arg = ''

    def __init__(self, api_token):
        self.api_token = api_token
        self.session = requests.Session()
        self.set_auth_header()

    def set_auth_header(self):
        raise NotImplementedError

    def get(self, request):
        return self.session.get(self.api_url + request)

    def post(self, request):
        return self.session.post(self.api_url + request)

    def get_stars(self):
        star_list, page = [], 1
        err(Style.RESET_ALL + 'Downloading star list from %s: page ' % self.name, end='')
        while True:
            err(page, end='', flush=True)
            data = self.get(self.starred_request + 'per_page=100&page=' + str(page))
            star_list.extend([d[self.path_arg] for d in data.json()])
            if 'next' not in data.links:
                err('')
                break
            page += 1
            err(',', end='')

        err(Style.RESET_ALL + Style.BRIGHT + 'Downloaded a list of %d starred repositories' % len(star_list))
        return star_list


class GitHub(Provider):
    name = 'GitHub'
    api_url = 'https://api.github.com'
    starred_request = '/user/starred?'
    path_arg = 'full_name'

    def set_auth_header(self):
        self.session.headers['Authorization'] = 'token %s' % self.api_token
        # elif hasattr(self, 'username') and hasattr(self, 'password'):
        # self.session.auth = (self.username, self.password)


class GitLab(Provider):
    name = 'GitLab'
    api_url = 'https://gitlab.com/api/v4'
    starred_request = '/projects?starred=true&simple=true&'
    path_arg = 'path_with_namespace'

    def set_auth_header(self):
        self.session.headers['PRIVATE-TOKEN'] = self.api_token


def star_on_gitlab(gitlab, star_list):
    count = dict(success=0, not_found=0, skip=0, error=0)

    for star in star_list:
        response = gitlab.post('/projects/%s/star' % star.replace('/', '%2F'))

        if response.status_code == 201:
            err(Style.RESET_ALL + Style.BRIGHT + Fore.GREEN + 'Found and starred %s on GitLab!' % star)
            count['success'] += 1
        elif response.status_code == 304:
            err(Style.RESET_ALL + Fore.YELLOW + 'Found %s on GitLab, but it was already starred' % star)
            count['skip'] += 1
        elif response.status_code == 404:
            err(Style.RESET_ALL + 'Not found on GitLab: %s' % star)
            count['not_found'] += 1
        else:
            err(Style.RESET_ALL + Fore.RED + 'Error: got HTTP %d while trying to star %s on GitLab' % (
                response.status_code, star))
            count['error'] += 1
    return count


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args=args)

    if not GITLAB_TOKEN:
        err(Style.RESET_ALL + 'GITLAB_TOKEN environment variable must be set')
        return 1

    gitlab = GitLab(GITLAB_TOKEN)

    if args.from_file is None:
        if not GITHUB_TOKEN:
            err(Style.RESET_ALL + 'GITHUB_TOKEN environment variable must be set')
            return 1

        github = GitHub(GITHUB_TOKEN)
        github_star_list = github.get_stars()

    else:
        with open(args.from_file) as stream:
            github_star_list = {line.rstrip('\n') for line in stream.readlines()} - {''}
        err(Style.RESET_ALL + Style.BRIGHT + 'Read a list of %d starred repositories' % len(github_star_list))

    if not args.no_pre_skip:
        gitlab_star_list = gitlab.get_stars()

        github_set = set(star.lower() for star in github_star_list)
        gitlab_set = set(star.lower() for star in gitlab_star_list)

        stars_to_sync = github_set - gitlab_set

        skipped = len(github_set) - len(stars_to_sync)
        if skipped > 0:
            err(Style.RESET_ALL + Fore.YELLOW + 'Skipping %d repositories that are already starred on GitLab' % skipped)

    else:
        skipped = 0
        stars_to_sync = github_star_list

    report = star_on_gitlab(gitlab, stars_to_sync)

    err(Style.RESET_ALL + Style.BRIGHT)
    err('---------- Report ----------')
    err('')
    err('Stars:     %d' % report['success'])
    err('Skipped:   %d' % (report['skip'] + skipped))
    err('Not found: %d' % report['not_found'])
    err('Errors:    %d' % report['error'])


if __name__ == '__main__':
    sys.exit(main())
