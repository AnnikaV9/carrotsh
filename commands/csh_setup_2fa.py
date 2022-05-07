import pyotp

def main(args):
    secret_key = pyotp.random_base32()
    secret_key_file = open("login/2fa_key", "w")
    secret_key_file.write(secret_key)
    secret_key_file.close()
    print("Secret Key: {}".format(secret_key))