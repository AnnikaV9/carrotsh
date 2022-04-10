from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import getpass
import logging
import json
import time
import sys

logging.basicConfig(format="%(asctime)s - %(message)s", filename="logins.log", filemode="a", level=logging.INFO)
logger = logging.getLogger()

try:
    config_file = open("config.json", "r")
    config = json.load(config_file)
    config_file.close()


    if not config["password_auth"]:
        if os.getenv("HOME") != None:
            os.chdir(os.getenv("HOME"))

        logger.info("Successful login")
        os.system(config["shell"])

    else:    
        password_file = open("shadow", "rb")
        password = password_file.read()
        password_file.close()
        if config["password_auth_options"]["show_username"]:
            prompt = "Password for {}: ".format(getpass.getuser())
            
        else:
            prompt = "Password: "

        try:
            given_password = getpass.getpass(prompt)
        
        except (EOFError, KeyboardInterrupt):
            print("Login cancelled.")
            logger.info("Cancelled login")
            sys.exit()

        kdf = Scrypt(salt=config["password_auth_options"]["salt"].encode(), length=32, n=2**14, r=8, p=1)
        if kdf.derive(given_password.encode()) == password:
            if os.getenv("HOME") != None:
                os.chdir(os.getenv("HOME"))

            logger.info("Successful login")
            os.system(config["shell"])

        else:
            time.sleep(3)
            print("Authentication failed.")
            logger.info("Failed login, incorrect password")
            sys.exit()

except SystemExit:
    None

except:
    logger.info(str(sys.exc_info()).replace("\n", " "))
