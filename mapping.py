import json

with open('mapping_data.json') as stream:
    data_array = json.load(stream)

mapping = {}

for dct in data_array:
    for provider, path in dct.items():
        mapping[provider + ':' + path] = dct
