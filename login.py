from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import getpass
import json
import time
import sys

config_file = open("config.json", "r")
config = json.load(config_file)
config_file.close()

if not config["password_auth"]:
    if os.getenv("HOME") != None:
        os.chdir(os.getenv("HOME"))
    os.system(config["shell"])

else:    
    password_file = open("shadow", "rb")
    password = password_file.read()
    password_file.close()

    given_password = getpass.getpass("Password for {}: ".format(getpass.getuser()))
    kdf = Scrypt(salt=config["salt"].encode(), length=32, n=2**14, r=8, p=1)
    if kdf.derive(given_password.encode()) == password:
        if os.getenv("HOME") != None:
            os.chdir(os.getenv("HOME"))
        os.system(config["shell"])

    else:
        time.sleep(3)
        print("Authentication failed.")
        sys.exit(1)
