"""
cmd: clear-auto-blocklist
"""

import json


def main(args: list) -> None:

    """
    Removes all addresses from blocklists/auto_blocklist.json
    """

    del args

    with open("blocklists/auto_blocklist.json", "r", encoding="utf-8") as auto_blocklist_file_for_read:
        auto_blocklist = json.load(auto_blocklist_file_for_read)

    auto_blocklist["blocklist"] = {}
    auto_blocklist["attempt_tracker"] = {}

    with open("blocklists/auto_blocklist.json", "w", encoding="utf-8") as auto_blocklist_file_for_write:
        json.dump(auto_blocklist, auto_blocklist_file_for_write, indent=4)

    print("Cleared the auto blocklist")
