import subprocess
import sys


def main(args: list) -> None:
    npm_install_cmd = ["npm", "install"]
    pip_install_cmd = [sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"]
    print(f"subprocess.run({npm_install_cmd})\n")
    status = subprocess.run(npm_install_cmd)
    print(f"\n{status}")
    print(f"\nsubprocess.run({pip_install_cmd})\n")
    status = subprocess.run(pip_install_cmd)
    print(f"\n{status}")

    return
