import json
import yaml
import sys
import subprocess

def syntax_check_json(f):
    try:
        target_file = open(f, "r")
        contents = json.load(target_file)
        target_file.close()

    except:
        sys.exit("ERROR: {} failed the json syntax check".format(f))
 
def syntax_check_yaml(f):
    try:
        target_file = open(f, "r")
        contents = yaml.safe_load(target_file)
        target_file.close()

    except:
        sys.exit("ERROR: {} failed the yaml syntax check".format(f))

def main(args):
    for f in [
        "blocklists/user_blocklist.json",
        "blocklists/auto_blocklist.json",
    ]:
        syntax_check_json(f)
    
    for f in [
        "config.yaml"
    ]:
        syntax_check_yaml(f)

    subprocess.run(["node_modules/pm2/bin/pm2", "start", "pm2.config.js"])
