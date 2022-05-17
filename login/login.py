from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import subprocess
import getpass
import logging
import json
import yaml
import time
import sys
import pyotp


class LoginManager:

    def __init__(self) -> None:
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            filename="login/logins.log",
            filemode="a",
            level=logging.INFO
        )
        self.logger = logging.getLogger()

        config_file = open("config.yaml", "r")
        self.config = yaml.safe_load(config_file)
        config_file.close()

        try:
            self.client_remote_address = sys.argv[1]

        except IndexError:
            self.client_remote_address = "Unknown"

        return

    def spawn_shell(self) -> None:
        if os.getenv("HOME") is not None:
            os.chdir(os.getenv("HOME"))

        subprocess.run(self.config["shell"])

        return

    def verify_otp(self) -> bool:
        try:
            user_otp = input("Enter the OTP shown in your authenticator app: ")

        except (EOFError, KeyboardInterrupt):
            self.logger.info("({}) Cancelled login".format(self.client_remote_address))
            print("Login cancelled.")
            sys.exit()

        secret_key_file = open("login/2fa_key", "r")
        secret_key = secret_key_file.read()
        secret_key_file.close()
        totp = pyotp.TOTP(secret_key)

        if totp.verify(user_otp):

            return True

        else:

            return False

    def verify_pass(self) -> bool:
        if self.config["password_auth_options"]["show_username"]:
            login_prompt = "Password for {}: ".format(getpass.getuser())

        else:
            login_prompt = "Password: "

        password_file = open("login/password", "rb")
        password = password_file.read()
        password_file.close()

        try:
            given_password = getpass.getpass(login_prompt)

        except (EOFError, KeyboardInterrupt):
            self.logger.info("({}) Cancelled login".format(self.client_remote_address))
            print("Login cancelled.")
            sys.exit()

        kdf = Scrypt(
            salt=self.config["password_auth_options"]["salt"].encode(),
            length=32,
            n=2**14,
            r=8,
            p=1
        )

        if kdf.derive(given_password.encode()) == password:

            return True

        else:

            return False

    def block(self) -> None:
        self.logger.info("({}) Login blocked, address in user blocklist".format(self.client_remote_address))
        if self.config["blocklist_shadow_mode"]:
            given_password = getpass.getpass(login_prompt)
            time.sleep(3)
            print("Authentication failed.")

        else:
            print("You have been blocked by the server.")

        sys.exit()

        return

    def main(self) -> None:
        try:
            if self.config["auto_blocklist"]:
                auto_blocklist_file = open("blocklists/auto_blocklist.json", "r")
                auto_blocklist = json.load(auto_blocklist_file)
                auto_blocklist_file.close()

                unblock = False
                for entry in auto_blocklist["blocklist"].keys():
                    if entry in self.client_remote_address:
                        if int(time.time()) > auto_blocklist["blocklist"][entry]:
                            unblock = True

                        else:
                            self.block()

                if unblock:
                    del auto_blocklist["blocklist"][entry]
                    auto_blocklist_file = open("blocklists/auto_blocklist.json", "w")
                    json.dump(auto_blocklist, auto_blocklist_file, indent=4)
                    auto_blocklist_file.close()

            user_blocklist_file = open("blocklists/user_blocklist.json", "r")
            user_blocklist = json.load(user_blocklist_file)
            user_blocklist_file.close()

            for entry in user_blocklist["blocklist"]:
                if entry in self.client_remote_address:
                    self.block()

            if not self.config["password_auth"]:
                if not self.config["2fa"]:
                    logged_in = True

                else:
                    if self.verify_otp():
                        logged_in = True

                    else:
                        logged_in = False

                if logged_in:
                    self.spawn_shell()

                else:
                    self.logger.info("({}) Failed login, incorrect otp".format(self.client_remote_address))
                    time.sleep(3)
                    print("Authentication failed.")
                    sys.exit()

            else:
                if self.verify_pass():
                    if not self.config["2fa"]:
                        logged_in = True

                    else:
                        if self.verify_otp():
                            logged_in = True

                        else:
                            logged_in = False

                    if logged_in:
                        self.spawn_shell()

                    else:
                        self.logger.info("({}) Failed login, incorrect otp".format(self.client_remote_address))
                        time.sleep(3)
                        print("Authentication failed.")
                        sys.exit()

                else:
                    if self.config["auto_blocklist"]:
                        if self.client_remote_address in auto_blocklist["attempt_tracker"].keys():
                            if auto_blocklist["attempt_tracker"][self.client_remote_address] < (config["auto_blocklist_options"]["max_incorrect_attemps"] - 1):
                                auto_blocklist["attempt_tracker"][self.client_remote_address] += 1

                            else:
                                auto_blocklist["blocklist"][self.client_remote_address] = int(time.time()) + (config["auto_blocklist_options"]["unblock_after_minutes"] * 60)
                                del auto_blocklist["attempt_tracker"][self.client_remote_address]

                        else:
                            auto_blocklist["attempt_tracker"][self.client_remote_address] = 1
                        auto_blocklist_file = open("blocklists/auto_blocklist.json", "w")
                        json.dump(auto_blocklist, auto_blocklist_file, indent=4)
                        auto_blocklist_file.close()

                    self.logger.info("({}) Failed login, incorrect password".format(client_remote_address))
                    time.sleep(3)
                    print("Authentication failed.")
                    sys.exit()

        except Exception:
            self.logger.info(str(sys.exc_info()).replace("\n", " "))
            print("An error occured during login.")

        return


if __name__ == "__main__":
    login_manager = LoginManager()
    LoginManager.main()
