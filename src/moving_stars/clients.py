# -*- coding: utf-8 -*-

import requests

from colorama import Fore, Style

from .utils import err
from .mapping import get_mapping

mapping = get_mapping()


class Provider(object):
    name = "Generic Provider"
    url = ""
    api_url = ""
    starred_request = ""
    star_request = ""
    path_arg = ""

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
        err(
            Style.RESET_ALL + "Downloading star list from %s: page " % self.name, end=""
        )
        while True:
            err(page, end="", flush=True)
            data = self.get(self.starred_request + "per_page=100&page=" + str(page))
            star_list.extend([d[self.path_arg] for d in data.json()])
            if "next" not in data.links:
                err("")
                break
            page += 1
            err(",", end="")

        err(
            Style.RESET_ALL
            + Style.BRIGHT
            + "Downloaded a list of %d starred repositories" % len(star_list)
        )
        return star_list

    def format_star_id(self, star):
        raise NotImplementedError

    def post_stars(self, star_list):
        count = dict(success=0, not_found=0, skip=0, error=0)

        for star in star_list:
            if star in mapping:
                star = mapping[star].get(self.url, star)

            response = self.post(self.star_request % self.format_star_id(star))

            if response.status_code == 201:
                err(
                    Style.RESET_ALL
                    + Style.BRIGHT
                    + Fore.GREEN
                    + "Found and starred %s on %s!" % (star, self.name)
                )
                count["success"] += 1
            elif response.status_code == 304:
                err(
                    Style.RESET_ALL
                    + Fore.YELLOW
                    + "Found %s on %s, but it was already starred" % (star, self.name)
                )
                count["skip"] += 1
            elif response.status_code == 404:
                err(Style.RESET_ALL + "Not found on %s: %s" % (self.name, star))
                count["not_found"] += 1
            else:
                err(
                    Style.RESET_ALL
                    + Fore.RED
                    + "Error: got HTTP %d while trying to star %s on %s"
                    % (response.status_code, star, self.name)
                )
                count["error"] += 1
        return count


class GitHub(Provider):
    name = "GitHub"
    url = "github.com"
    api_url = "https://api.github.com"
    starred_request = "/user/starred?"

    # TODO
    star_request = ""

    path_arg = "full_name"

    def set_auth_header(self):
        self.session.headers["Authorization"] = "token %s" % self.api_token
        # elif hasattr(self, 'username') and hasattr(self, 'password'):
        # self.session.auth = (self.username, self.password)

    def format_star_id(self, star):
        # TODO
        return star


class GitLab(Provider):
    name = "GitLab"
    url = "gitlab.com"
    api_url = "https://gitlab.com/api/v4"
    starred_request = "/projects?starred=true&simple=true&"
    star_request = "/projects/%s/star"
    path_arg = "path_with_namespace"

    def set_auth_header(self):
        self.session.headers["PRIVATE-TOKEN"] = self.api_token

    def format_star_id(self, star):
        return star.replace("/", "%2F")
