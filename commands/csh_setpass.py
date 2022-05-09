from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import getpass
import yaml
import sys

def obt_pass():
    password = getpass.getpass("New password: ")
    if getpass.getpass("Confirm password: ") != password:
        print("Error: Passwords do not match.")
        sys.exit(1)
    
    return password

def main(args):
    config_file = open("config.yaml", "r")
    config = yaml.safe_load(config_file)
    config_file.close()
    kdf = Scrypt(
        salt=config["password_auth_options"]["salt"].encode(),
        length=32,
        n=2**14,
        r=8,
        p=1
    )
    password_file = open("login/password", "wb")
    password_file.write(kdf.derive(obt_pass().encode()))
    password_file.close()
    print("Password saved.")
