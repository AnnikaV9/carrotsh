import json

def main(args):
   if len(args) < 3:
        sys.exit("ERROR: Missing argument: <address>")

    user_blocklist_file = open("blocklists/user_blocklist.json", "r")
    user_blocklist = json.load(user_blocklist_file)
    user_blocklist_file.close()
    user_blocklist["blocklist"].append(args[2])
    user_blocklist_file = open("blocklists/user_blocklist.json", "w")
    json.dump(user_blocklist, user_blocklist_file, indent=4)
    user_blocklist_file.close()
    print("Added {} to the user blocklist".format(args[2]))