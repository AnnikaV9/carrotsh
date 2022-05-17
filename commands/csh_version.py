import json


def main(args: list) -> None:
    package_file = open("package.json", "r")
    version = json.load(package_file)["version"]
    package_file.close()
    print("carrotsh v{}".format(version))

    return
