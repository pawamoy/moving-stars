# -*- coding: utf-8 -*-

import pytoml
import requests


def get_mapping():
    response = requests.get('https://gitlab.com/pawamoy/foss-map-data/raw/master/data.toml').text
    data_array = pytoml.loads(response).get("data", [])

    mapping = {}

    for dct in data_array:
        for provider, path in dct.items():
            mapping[provider + ":" + path] = dct

    return mapping
