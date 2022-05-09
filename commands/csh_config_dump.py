import yaml
import json

def main(args):
    config_file = open("config.json", "r")
    config = yaml.safe_load(config_file)
    config_file.close()
    print(json.dumps(config, indent=4))
