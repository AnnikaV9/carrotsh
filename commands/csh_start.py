"""
cmd: start
"""

import json
import sys
import subprocess


def syntax_check_json(target_file: str) -> None:

    """
    Checks if a json file has invalid syntax
    """

    try:
        with open(target_file, "r", encoding="utf-8") as file_to_check:
            contents = json.load(file_to_check)

        del contents

    except json.decoder.JSONDecodeError:
        sys.exit(f"ERROR: {target_file} failed the json syntax check")


def main(args: list) -> None:

    """
    Runs the syntax check on blocklists/user_blocklist.json and
    blocklists/auto_blocklist.json. Then starts the server by
    running `node_modules/pm2/bin/pm2 start pm2.config.js`
    """

    del args

    for suspect in [
        "blocklists/user_blocklist.json",
        "blocklists/auto_blocklist.json"
    ]:
        syntax_check_json(suspect)

    subprocess.run(["node_modules/pm2/bin/pm2", "start", "pm2.config.js"], check=True)
