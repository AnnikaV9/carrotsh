"""
cmd: install-blocklist
"""

import json
import sys


def main(args: list) -> None:

    """
    Copies over addresses from specified file to blocklists/user_blocklist.json
    and removes any # comments
    """

    if len(args) < 3:
        sys.exit("ERROR: Missing argument: </path/to/list>")

    with open(args[2], "r", encoding="utf-8") as new_blocklist_file:
        new_blocklist_raw = new_blocklist_file.read()

    new_blocklist = new_blocklist_raw.split("\n")

    to_remove = []

    for entry in new_blocklist:
        if "#" in entry:
            to_remove.append(entry)

    if len(to_remove) > 0:
        for entry in to_remove:
            new_blocklist.remove(entry)

    new_blocklist.remove("")

    with open("blocklists/user_blocklist.json", "r", encoding="utf-8") as user_blocklist_file_for_read:
        user_blocklist = json.load(user_blocklist_file_for_read)

    user_blocklist["blocklist"].extend(new_blocklist)

    with open("blocklists/user_blocklist.json", "w", encoding="utf-8") as user_blocklist_file_for_write:
        json.dump(user_blocklist, user_blocklist_file_for_write, indent=4)

    print(f"Copied {len(new_blocklist)} addresses from {args[2]}")
