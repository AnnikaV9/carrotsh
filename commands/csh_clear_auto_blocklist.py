import json


def main(args: list) -> None:
    auto_blocklist_file = open("blocklists/auto_blocklist.json", "r")
    auto_blocklist = json.load(auto_blocklist_file)
    auto_blocklist_file.close()
    auto_blocklist["blocklist"] = {}
    auto_blocklist["attempt_tracker"] = {}
    auto_blocklist_file = open("blocklists/auto_blocklist.json", "w")
    json.dump(auto_blocklist, auto_blocklist_file, indent=4)
    auto_blocklist_file.close()
    print("Cleared the auto blocklist")

    return
