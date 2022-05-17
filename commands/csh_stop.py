import subprocess


def main(args: list) -> None:
    subprocess.run(["node_modules/pm2/bin/pm2", "delete", "pm2.config.js"])

    return
