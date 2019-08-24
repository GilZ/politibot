from os import path
import json

config_dir = path.join(path.dirname(__file__), '..', '..', 'config')


def get_config(config_name):
    with open(path.join(config_dir, config_name + '.json')) as f:
        return json.load(f)
