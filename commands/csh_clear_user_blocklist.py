import json

def main(args):
    user_blocklist_file = open("blocklists/user_blocklist.json", "r")
    user_blocklist = json.load(user_blocklist_file)
    user_blocklist_file.close()
    user_blocklist["blocklist"] = []
    user_blocklist_file = open("blocklists/user_blocklist.json", "w")
    json.dump(user_blocklist, user_blocklist_file, indent=4)
    user_blocklist_file.close()
    print("Cleared the user blocklist")