"""
cmd: install-deps
"""

import subprocess


def main(args: list) -> None:

    """
    Installs npm dependencies with `npm install` and
    installs python dependencies to a virtualenv with
    `poetry install`
    """

    del args

    npm_install_cmd = ["npm", "install"]
    poetry_install_cmd = ["poetry", "install"]
    print(f"subprocess.run({npm_install_cmd})\n")
    status = subprocess.run(npm_install_cmd, check=True)
    print(f"\n{status}")
    print(f"\nsubprocess.run({poetry_install_cmd})\n")
    status = subprocess.run(poetry_install_cmd, check=True)
    print(f"\n{status}")
