"""
cmd: config-dump
"""

import json
import yaml


def main(args: list) -> None:

    """
    Reads config.yaml and dumps data to console in json
    """

    del args

    with open("config.yaml", "r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    print(json.dumps(config, indent=4))
