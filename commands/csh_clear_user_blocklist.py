"""
cmd: clear-user-blocklist
"""

import json


def main(args: list) -> None:

    """
    Removes all addresses from blocklists/user_blocklist.json
    """

    del args

    with open("blocklists/user_blocklist.json", "r", encoding="utf-8") as user_blocklist_file_for_read:
        user_blocklist = json.load(user_blocklist_file_for_read)

    user_blocklist["blocklist"] = []

    with open("blocklists/user_blocklist.json", "w", encoding="utf-8") as user_blocklist_file_for_write:
        json.dump(user_blocklist, user_blocklist_file_for_write, indent=4)

    print("Cleared the user blocklist")
