import sys
import os


if __name__ == "__main__":
    help_message = """
usage: python3 csh <COMMAND> [args]

commands:

    help                                  show this message
    version                               output the version information
    start                                 run a syntax check and start the carrosh server
    stop                                  stop the carrotsh server
    status                                show the current status of the server
    setpass                               set the server password
    setup-2fa                             setup 2-factor authentication
    clear-auto-blocklist                  clear the auto blocklist
    clear-user-blocklist                  clear the user blocklist
    add-blocklist-address <address>       add an address to the user blocklist
    install-blocklist </path/to/list>     copy addresses in a file to the user blocklist
    config-dump                           dump all configuration options to the terminal
    install-deps                          install npm and pip dependencies

"""

    if len(sys.argv) < 2 or "--help" == sys.argv[1] or "-h" == sys.argv[1] or "help" == sys.argv[1]:
        sys.exit(help_message)

    commands = [
        "version",
        "start",
        "stop",
        "status",
        "setpass",
        "setup-2fa",
        "clear-auto-blocklist",
        "clear-user-blocklist",
        "add-blocklist-address",
        "install-blocklist",
        "config-dump",
        "install-deps"
    ]

    if sys.argv[1] not in commands:
        sys.exit("ERROR: Unknown command {}".format(sys.argv[1]))

    sys.path.insert(0, "{}/commands".format(os.getcwd()))

    command = sys.argv[1].replace("-", "_")

    __import__("csh_{}".format(command)).main(sys.argv)
