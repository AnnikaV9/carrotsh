import json
import sys
import subprocess

def syntax_check(f):
    try:
        target_file = open(f, "r")
        contents = json.load(target_file)
        target_file.close()

    except:
        sys.exit("ERROR: {} failed the json syntax check".format(f))

def main(args):
    for f in [
        "blocklists/user_blocklist.json",
        "blocklists/auto_blocklist.json",
        "config.json"
        ]:
        syntax_check(f)
    subprocess.run(["node_modules/pm2/bin/pm2", "start", "server/server.js", "--name", "carrotsh"])
