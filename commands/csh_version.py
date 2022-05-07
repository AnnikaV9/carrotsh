import json

def main(args):
    package_file = open("package.json", "r")
    version = json.load(package_file)["version"]
    package_file.close()
    print("carrotsh v{}".format(version))