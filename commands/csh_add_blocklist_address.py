"""
cmd: add-blocklist-address
"""

import json
import sys


def main(args: list) -> None:

    """
    Adds a single address to blocklists/user_blocklist.json
    """

    if len(args) < 3:
        sys.exit("ERROR: Missing argument: <address>")

    with open("blocklists/user_blocklist.json", "r", encoding="utf-8") as user_blocklist_file_for_read:
        user_blocklist = json.load(user_blocklist_file_for_read)

    user_blocklist["blocklist"].append(args[2])

    with open("blocklists/user_blocklist.json", "w", encoding="utf-8") as user_blocklist_file_for_write:
        json.dump(user_blocklist, user_blocklist_file_for_write, indent=4)

    print(f"Added {args[2]} to the user blocklist")
