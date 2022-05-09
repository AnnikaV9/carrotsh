import subprocess

def main(args):
    subprocess.run(["node_modules/pm2/bin/pm2", "delete", "pm2.config.js"])
