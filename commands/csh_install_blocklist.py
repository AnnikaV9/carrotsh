import json
import sys


def main(args: list) -> None:
    if len(args) < 3:
        sys.exit("ERROR: Missing argument: </path/to/list>")

    new_blocklist_file = open(args[2], "r")
    new_blocklist_raw = new_blocklist_file.read()
    new_blocklist_file.close()

    new_blocklist = new_blocklist_raw.split("\n")

    to_remove = []
    for entry in new_blocklist:
        if "#" in entry:
            to_remove.append(entry)

    if len(to_remove) > 0:
        for entry in to_remove:
            new_blocklist.remove(entry)

    new_blocklist.remove("")

    user_blocklist_file = open("blocklists/user_blocklist.json", "r")
    user_blocklist = json.load(user_blocklist_file)
    user_blocklist_file.close()

    user_blocklist["blocklist"].extend(new_blocklist)

    user_blocklist_file = open("blocklists/user_blocklist.json", "w")
    json.dump(user_blocklist, user_blocklist_file, indent=4)
    user_blocklist_file.close()

    print("Copied {} addresses from {}".format(len(new_blocklist), args[2]))

    return
