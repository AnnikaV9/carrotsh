"""
cmd: setpass
"""

import sys
import getpass
import yaml
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def obt_pass() -> str:

    """
    Prompts the user for a password, and matches the input with a second second prompt
    """

    password = getpass.getpass("New password: ")
    if getpass.getpass("Confirm password: ") != password:
        print("Error: Passwords do not match.")
        sys.exit(1)

    return password


def main(args: list) -> None:

    """
    Hashes the password with configured salt and writes the data to login/password
    """

    del args

    with open("config.yaml", "r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    kdf = Scrypt(
        salt=config["password_auth_options"]["salt"].encode(),
        length=32,
        n=2**14,
        r=8,
        p=1
    )

    with open("login/password", "wb") as password_file:
        password_file.write(kdf.derive(obt_pass().encode()))

    print("Password saved.")
