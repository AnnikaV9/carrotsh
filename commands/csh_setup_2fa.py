"""
cmd: setup-2fa
"""

import pyotp


def main(args: list) -> None:

    """
    Generates a random secret key, saves it, and prints it to the console
    """

    del args

    secret_key = pyotp.random_base32()

    with open("login/2fa_key", "w", encoding="utf-8") as secret_key_file:
        secret_key_file.write(secret_key)

    print(f"Secret Key: {secret_key}")
