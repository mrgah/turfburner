import json

def get_config(config_fn='config.json'):
    with open(config_fn) as fh:
        configs = json.load(fh)
    return configs
