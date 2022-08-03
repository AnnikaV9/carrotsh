"""
cmd: stop
"""

import subprocess


def main(args: list) -> None:

    """
    Stops the server by running
    `node_modules/pm2/bin/pm2 delete pm2.config.js`
    """

    del args

    subprocess.run(["node_modules/pm2/bin/pm2", "delete", "pm2.config.js"], check=True)
