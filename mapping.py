import pytoml

with open('mapping_data.toml') as stream:
    data_array = pytoml.load(stream).get('data', [])

mapping = {}

for dct in data_array:
    for provider, path in dct.items():
        mapping[provider + ':' + path] = dct
