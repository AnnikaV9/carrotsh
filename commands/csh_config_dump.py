import json

def main(args):
    config_file = open("config.json", "r")
    config = json.load(config_file)
    config_file.close()
    print(json.dumps(config, indent=4))
