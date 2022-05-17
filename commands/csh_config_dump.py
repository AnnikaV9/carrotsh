import yaml
import json


def main(args: list) -> None:
    config_file = open("config.yaml", "r")
    config = yaml.safe_load(config_file)
    config_file.close()
    print(json.dumps(config, indent=4))

    return
