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
        
    user_blocklist_file = open("user_blocklist.json", "r")
    user_blocklist = json.load(user_blocklist_file)
    user_blocklist_file.close()

    auto_blocklist_file = open("auto_blocklist.json", "r")
    auto_blocklist = json.load(auto_blocklist_file)
    auto_blocklist_file.close()

    try:
        client_remote_address = sys.argv[1]
    
    except IndexError:
        client_remote_address = "Unknown"

    if config["password_auth_options"]["show_username"]:
        login_prompt = "Password for {}: ".format(getpass.getuser())
            
    else:
        login_prompt = "Password: "
    
    if config["auto_blocklist"]:
        unblock = False
        for entry in auto_blocklist["blocklist"].keys():
            if entry in client_remote_address:
                if int(time.time()) > auto_blocklist["blocklist"][entry]:
                    unblock = True
                

                else:
                    logger.info("({}) Login blocked, address in auto blocklist".format(client_remote_address))
                    if config["blocklist_shadow_mode"]:
                        given_password = getpass.getpass(login_prompt)
                        time.sleep(3)
                        print("Authentication failed.")
                        sys.exit()
                
                    else:
                        print("You have been automatically blocked by the server.")
                        sys.exit()
        
        if unblock:
            del auto_blocklist["blocklist"][entry]
            auto_blocklist_file = open("auto_blocklist.json", "w")
            json.dump(auto_blocklist, auto_blocklist_file, indent=4)
            auto_blocklist_file.close()
                
    for entry in user_blocklist["blocklist"]:
        if entry in client_remote_address:
            logger.info("({}) Login blocked, address in user blocklist".format(client_remote_address))
            if config["blocklist_shadow_mode"]:
                given_password = getpass.getpass(login_prompt)
                time.sleep(3)
                print("Authentication failed.")
                sys.exit()
            
            else:
                print("You have been blocked by the server admin.")
                sys.exit()

            
    if not config["password_auth"]:
        if os.getenv("HOME") != None:
            os.chdir(os.getenv("HOME"))

        logger.info("({}) Successful login".format(client_remote_address))
        os.system(config["shell"])

    else:    
        password_file = open("shadow", "rb")
        password = password_file.read()
        password_file.close()

        try:
            given_password = getpass.getpass(login_prompt)
        
        except (EOFError, KeyboardInterrupt):
            logger.info("({}) Cancelled login".format(client_remote_address))
            print("Login cancelled.")
            sys.exit()

        kdf = Scrypt(salt=config["password_auth_options"]["salt"].encode(), length=32, n=2**14, r=8, p=1)
        if kdf.derive(given_password.encode()) == password:
            if os.getenv("HOME") != None:
                os.chdir(os.getenv("HOME"))

            logger.info("({}) Successful login".format(client_remote_address))
            os.system(config["shell"])

        else:
            if config["auto_blocklist"]:
                if client_remote_address in auto_blocklist["attempt_tracker"].keys():
                    if auto_blocklist["attempt_tracker"][client_remote_address] < (config["auto_blocklist_options"]["max_incorrect_attemps"] - 1):
                        auto_blocklist["attempt_tracker"][client_remote_address] += 1
                    
                    else:
                        auto_blocklist["blocklist"][client_remote_address] = int(time.time()) + (config["auto_blocklist_options"]["unblock_after_minutes"] * 60)
                        del auto_blocklist["attempt_tracker"][client_remote_address]
                
                else:
                    auto_blocklist["attempt_tracker"][client_remote_address] = 1
                auto_blocklist_file = open("auto_blocklist.json", "w")
                json.dump(auto_blocklist, auto_blocklist_file, indent=4)
                auto_blocklist_file.close()

            logger.info("({}) Failed login, incorrect password".format(client_remote_address))
            time.sleep(3)
            print("Authentication failed.")
            sys.exit()

except SystemExit:
    None

except:
    logger.info(str(sys.exc_info()).replace("\n", " "))
    print("An error occured during login.")
