import subprocess
import sys


def main(args: list) -> None:
    npm_install_cmd = ["npm", "install"]
    poetry_install_cmd = ["poetry", "install"]
    print(f"subprocess.run({npm_install_cmd})\n")
    status = subprocess.run(npm_install_cmd)
    print(f"\n{status}")
    print(f"\nsubprocess.run({poetry_install_cmd})\n")
    status = subprocess.run(poetry_install_cmd)
    print(f"\n{status}")

    return
