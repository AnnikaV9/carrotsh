import json
import sys
import subprocess


def syntax_check_json(f: str) -> None:
    try:
        target_file = open(f, "r")
        contents = json.load(target_file)
        target_file.close()

    except json.decoder.JSONDecodeError:
        sys.exit("ERROR: {} failed the json syntax check".format(f))

    return


def main(args: list) -> None:
    for f in [
        "blocklists/user_blocklist.json",
        "blocklists/auto_blocklist.json"
    ]:
        syntax_check_json(f)

    subprocess.run(["node_modules/pm2/bin/pm2", "start", "pm2.config.js"])

    return
