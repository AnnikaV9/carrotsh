"""
cmd: version
"""

import json


def main(args: list) -> None:

    """
    Checks the server version in package.json and prints
    it to the console
    """

    del args

    with open("package.json", "r", encoding="utf-8") as package_file:
        version = json.load(package_file)["version"]

    print(f"carrotsh v{version}")
