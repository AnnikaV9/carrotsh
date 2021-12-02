from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import getpass
import json
import sys

print("--- Password setup for carrotsh ---\n")
password = getpass.getpass("New password: ")
if getpass.getpass("Confirm password: ") != password:
    print("Error: Passwords do not match.")
    sys.exit(1)

else:
    config_file = open("config.json", "r")
    config = json.load(config_file)
    config_file.close()
    kdf = Scrypt(salt=config["salt"].encode(), length=32, n=2**14, r=8, p=1)
    password_file = open("shadow", "wb")
    password_file.write(kdf.derive(password.encode()))
    password_file.close()
    print("Password saved.\n")
