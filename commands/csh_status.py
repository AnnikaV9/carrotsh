"""
cmd: status
"""

import subprocess


def main(args: list) -> None:

    """
    Outputs server status by running
    `node_modules/pm2/bin/pm2 info carrotsh`
    """

    del args

    subprocess.run(["node_modules/pm2/bin/pm2", "info", "carrotsh"], check=True)
