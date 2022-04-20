import sys
import json
import os

help_message = """
Usage: python3 carrotsh.py <COMMAND> [args]


A CLI wrapper for carrotsh scripts


Commands:

version                               output the version
start                                 run a syntax check and start the carrosh server
stop                                  stop the carrotsh server
setpass                               set the server password
clear-auto-blocklist                  clear the auto blocklist
clear-user-blocklist                  clear the user blocklist
add-blocklist-address <address>       add an address to the user blocklist
install-blocklist </path/to/list>     copy addresses in a file to the user blocklist
config-dump                           dump all configuration options to the terminal
"""

if len(sys.argv) < 2 or "--help" in sys.argv:
    sys.exit(help_message)

commands = [
    "version",
    "start",
    "stop",
    "setpass",
    "clear-auto-blocklist",
    "clear-user-blocklist",
    "add-blocklist-address",
    "install-blocklist",
    "config-set",
    "config-dump"
]

if sys.argv[1] not in commands:
    sys.exit("ERROR: Unknown command {}".format(sys.argv[1]))

command = sys.argv[1]

config_file = open("config.json", "r")
config = json.load(config_file)
config_file.close()

if command == "version":
    package_file = open("package.json", "r")
    version = json.load(package_file)["version"]
    package_file.close()
    print("carrotsh v{}".format(version))

elif command == "start":

    try:
        user_blocklist_file = open("blocklists/user_blocklist.json", "r")
        user_blocklist = json.load(user_blocklist_file)
        user_blocklist_file.close()

    except:
        sys.exit("ERROR: user_blocklist.json failed the json syntax check")

    try:
        auto_blocklist_file = open("blocklists/auto_blocklist.json", "r")
        auto_blocklist = json.load(auto_blocklist_file)
        auto_blocklist_file.close()

    except:
        sys.exit("ERROR: auto_blocklist.json failed the json syntax check")
    
    os.system("node_modules/pm2/bin/pm2 start server/server.js --name carrotsh")

elif command == "stop":
    os.system("node_modules/pm2/bin/pm2 delete carrotsh")

elif command == "setpass":
    os.system("{} scripts/setpass.py".format(config["python_path"]))

elif command == "clear-auto-blocklist":
    auto_blocklist_file = open("blocklists/auto_blocklist.json", "r")
    auto_blocklist = json.load(auto_blocklist_file)
    auto_blocklist_file.close()
    auto_blocklist["blocklist"] = {}
    auto_blocklist["attempt_tracker"] = {}
    auto_blocklist_file = open("blocklists/auto_blocklist.json", "w")
    json.dump(auto_blocklist, auto_blocklist_file, indent=4)
    auto_blocklist_file.close()
    print("Cleared the auto blocklist")

elif command == "clear-user-blocklist":
    user_blocklist_file = open("blocklists/user_blocklist.json", "r")
    user_blocklist = json.load(user_blocklist_file)
    user_blocklist_file.close()
    user_blocklist["blocklist"] = []
    user_blocklist_file = open("blocklists/user_blocklist.json", "w")
    json.dump(user_blocklist, user_blocklist_file, indent=4)
    user_blocklist_file.close()
    print("Cleared the user blocklist")

elif command == "add-blocklist-address":
    if len(sys.argv) < 3:
        sys.exit("ERROR: Missing argument: <address>")

    user_blocklist_file = open("blocklists/user_blocklist.json", "r")
    user_blocklist = json.load(user_blocklist_file)
    user_blocklist_file.close()
    user_blocklist["blocklist"].append(sys.argv[2])
    user_blocklist_file = open("blocklists/user_blocklist.json", "w")
    json.dump(user_blocklist, user_blocklist_file, indent=4)
    user_blocklist_file.close()
    print("Added {} to the user blocklist".format(sys.argv[2]))

elif command == "install-blocklist":
    if len(sys.argv) < 3:
        sys.exit("ERROR: Missing argument: </path/to/list>")
    
    os.system("{} scripts/blocklist_install.py {}".format(config["python_path"], sys.argv[2]))

elif command == "config-dump":
    config_file = open("config.json", "r")
    config = json.load(config_file)
    config_file.close()
    print(json.dumps(config, indent=4))
