import argparse
import base64
import getpass
import hashlib
import os

from coco_cli_modules.share.vaults import (
    get_vault_signature_from_filesystem
)
from coco_cli_modules.share.encryption import (
    generate_fernet_key
)


def main(*args):
    parser = argparse.ArgumentParser(
        description="Create an encrypted login inside of a vault"
    )
    parser.add_argument("login_name", metavar="login_name",
                        help="name for the login, ex. jimmy@hotmail.com")
    parser.add_argument("vault_location", metavar="vault",  # TODO: smart id
                        help="vault to store the login inside of")
    parser.add_argument("--tag", help="shorthand tag for the login")

    # change to display correct program name on parsing error, even though we
    # call this main procedure from another module (coco-cli.py)
    parser.prog = __file__.split("/")[-1]
    args = parser.parse_args(args)

    vault_signature_location = "{}/.cocovault".format(args.vault_location)
    if not os.path.exists(vault_signature_location):
        print("Error: cannot find vault at specified location")
        print(vault_signature_location)
        exit(-1)

    vsalt, vhash = get_vault_signature_from_filesystem(vault_signature_location)

    vault_has_key = os.path.exists("{}/id_fernet".format(args.vault_location))
    if vault_has_key:
        with open("{}/id_fernet".format(args.vault_location)) as keyfile:
            key = keyfile.read()
    else:
        user_pass = getpass.getpass("Enter the password for this vault: ")
        password_bytes = user_pass.encode('utf-8')
        user_hash = hashlib.sha256(password_bytes).digest()
        hash64 = base64.b64encode(user_hash).decode('utf-8')
        if hash64 != vhash:
            print("Error: password entered does not match the password for this vault.")
            print("Exiting.")
            print(vhash)
            print(hash64)
            exit(-1)
        else:
            key = generate_fernet_key(vsalt.encode('utf-8'), password_bytes)
    key_hash = hashlib.sha256(base64.b64decode(key)).hexdigest()
    print("Succesfully obtained fernet key with hash:\n{}".format(key_hash))
