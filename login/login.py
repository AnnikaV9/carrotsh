"""
The heart of carrotsh, this manages everything related to
logging into the server and running the shell/program
"""

import os
import time
import sys
import json
import subprocess
import logging
import getpass
import yaml
import pyotp
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt



class LoginManager:

    """
    The main LoginManager class
    """

    def __init__(self) -> None:

        """
        Initialize the logger, load the config and define define
        the client_remote_address variable
        """

        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            filename="login/logins.log",
            filemode="a",
            level=logging.INFO
        )
        self.logger = logging.getLogger()

        with open("config.yaml", "r", encoding="utf-8") as config_file:
            self.config = yaml.safe_load(config_file)

        try:
            self.client_remote_address = sys.argv[1]

        except IndexError:
            self.client_remote_address = "Unknown"

    def spawn_shell(self) -> None:

        """
        If $HOME is set then chdir()s to it,
        runs `stty cols 999` to fix the text wraparound issue
        and starts the shell
        """

        if os.getenv("HOME") is not None:
            os.chdir(os.getenv("HOME"))

        try:                                                       # Implement dynamic resizing of
            subprocess.run(["stty", "cols", "999"], check=False)   # the tty in server/server.js with
                                                                   # node-pty instead of this stupid
        except Exception:                                          # hacky fix that causes a lot of
            pass                                                   # programs like htop to look broken

        subprocess.run(self.config["shell"], check=False)

    def verify_otp(self) -> bool:

        """
        Obtains OTP from the user attempting to login, checks it
        against the server key and return a boolean value depending
        on whether the check passed or failed
        """

        try:
            user_otp = input("Enter the OTP shown in your authenticator app: ")

        except (EOFError, KeyboardInterrupt):
            self.logger.info("(%s) Cancelled login", self.client_remote_address)
            print("Login cancelled.")
            sys.exit()

        with open("login/2fa_key", "r", encoding="utf-8") as secret_key_file:
            secret_key = secret_key_file.read()

        return bool(pyotp.TOTP(secret_key).verify(user_otp))

    def verify_pass(self) -> bool:

        """
        Obtains password from the user attempting to login, hashes and
        checks it against the server hash, and returns a boolean value
        depending on whether the check passed or failed
        """

        if self.config["password_auth_options"]["show_username"]:
            login_prompt = f"Password for {getpass.getuser()}: "

        else:
            login_prompt = "Password: "

        with open("login/password", "rb") as password_file:
            password = password_file.read()

        try:
            given_password = getpass.getpass(login_prompt)

        except (EOFError, KeyboardInterrupt):
            self.logger.info("(%s) Cancelled login", self.client_remote_address)
            print("Login cancelled.")
            sys.exit()

        kdf = Scrypt(
            salt=self.config["password_auth_options"]["salt"].encode(),
            length=32,
            n=2**14,
            r=8,
            p=1
        )

        return bool(kdf.derive(given_password.encode()) == password)

    def block(self) -> None:

        """
        Blocks the user attempting to login
        """

        self.logger.info("(%s) Login blocked, address in user blocklist", self.client_remote_address)

        if self.config["blocklist_shadow_mode"]:
            getpass.getpass("Password: ")
            time.sleep(3)
            print("Authentication failed.")

        else:
            print("You have been blocked by the server.")

        sys.exit()

    def main(self) -> None:

        """
        The main function that manages everything
        """

        try:
            if self.config["auto_blocklist"]:
                with open("blocklists/auto_blocklist.json", "r", encoding="utf-8") as auto_blocklist_file:
                    auto_blocklist = json.load(auto_blocklist_file)

                unblock = False

                for entry in auto_blocklist["blocklist"].keys():
                    if entry in self.client_remote_address:
                        if int(time.time()) > auto_blocklist["blocklist"][entry]:
                            entry_to_remove = entry
                            unblock = True

                        else:
                            self.block()

                if unblock:
                    del auto_blocklist["blocklist"][entry_to_remove]
                    with open("blocklists/auto_blocklist.json", "w", encoding="utf-8") as auto_blocklist_file:
                        json.dump(auto_blocklist, auto_blocklist_file, indent=4)

            with open("blocklists/user_blocklist.json", "r", encoding="utf-8") as user_blocklist_file:
                user_blocklist = json.load(user_blocklist_file)

            for entry in user_blocklist["blocklist"]:
                if entry in self.client_remote_address:
                    self.block()

            if not self.config["password_auth"]:
                if not self.config["2fa"]:
                    logged_in = True

                else:
                    logged_in = self.verify_otp()

                if logged_in:
                    self.spawn_shell()

                else:
                    self.logger.info("(%s) Failed login, incorrect otp", self.client_remote_address)
                    time.sleep(3)
                    print("Authentication failed.")
                    sys.exit()

            else:
                if self.verify_pass():
                    if not self.config["2fa"]:
                        logged_in = True

                    else:
                        logged_in = self.verify_otp()

                    if logged_in:
                        self.spawn_shell()

                    else:
                        self.logger.info("(%s) Failed login, incorrect otp", self.client_remote_address)
                        time.sleep(3)
                        print("Authentication failed.")
                        sys.exit()

                else:
                    if self.config["auto_blocklist"]:
                        if self.client_remote_address in auto_blocklist["attempt_tracker"].keys():
                            if auto_blocklist["attempt_tracker"][self.client_remote_address] < (self.config["auto_blocklist_options"]["max_incorrect_attemps"] - 1):
                                auto_blocklist["attempt_tracker"][self.client_remote_address] += 1

                            else:
                                auto_blocklist["blocklist"][self.client_remote_address] = int(time.time()) + (self.config["auto_blocklist_options"]["unblock_after_minutes"] * 60)
                                del auto_blocklist["attempt_tracker"][self.client_remote_address]

                        else:
                            auto_blocklist["attempt_tracker"][self.client_remote_address] = 1
                        with open("blocklists/auto_blocklist.json", "w", encoding="utf-8") as auto_blocklist_file:
                            json.dump(auto_blocklist, auto_blocklist_file, indent=4)

                    self.logger.info("(%s) Failed login, incorrect password", self.client_remote_address)
                    time.sleep(3)
                    print("Authentication failed.")
                    sys.exit()

        except (KeyboardInterrupt, EOFError):
            self.logger.info("(%s) Cancelled login", self.client_remote_address)
            print("Login cancelled.")
            sys.exit()

        except Exception:
            self.logger.info(str(sys.exc_info()).replace("\n", " "))
            print("An error occured during login.")


if __name__ == "__main__":
    login_manager = LoginManager()
    login_manager.main()
    