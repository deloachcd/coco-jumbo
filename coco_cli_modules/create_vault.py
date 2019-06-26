import argparse
from base64 import b64encode
import hashlib
import json
import os

import getpass

from coco_cli_modules.share.constants import (
    SALT_SIZE,
    VAULT_ID_SIZE,
    DEFAULT_CONFIG_DIR
)
from coco_cli_modules.share.encryption import (
    generate_fernet_key
)


def not_a_directory_error():
    print("Error: vault location requested is not a directory.")
    exit(-1)


def main(*args):
    # args: {vault_location} [ --tag {vault_tags} ]
    parser = argparse.ArgumentParser(
        description=None
    )
    # change to display correct program name on parsing error, even though we
    # call this main procedure from another module (coco-cli.py)
    parser.prog = __file__.split("/")[-1]
    parser.add_argument('vault_location', metavar='vault-location',
                        help='location of directory to create vault within')
    parser.add_argument('--tag', help='shorthand tag for the new vault')
    args = parser.parse_args(args)

    vault_location = os.path.expanduser(args.vault_location)
    if not os.path.exists(vault_location):
        try:
            os.makedirs(vault_location)
        except NotADirectoryError:
            not_a_directory_error()
    elif not os.path.isdir(vault_location):
        not_a_directory_error()

    vault_signature_location = "{}/.cocovault".format(vault_location)
    if os.path.exists(vault_signature_location):
        print("Warning: A Coco Jumbo vault appears to already exist here.")
        print("You should only overwrite its signature (salt + password hash)\n"
              "if you really know what you're doing.\n")
        answer = input("Do you still want to overwrite it? (y/n) ").lower()
        if 'y' not in answer:
            print("Aborting.")
            exit()
        else:
            vaults_map_location = "{}/vaults.json".format(DEFAULT_CONFIG_DIR)
            if os.path.exists(vaults_map_location):
                with open(vaults_map_location, 'r') as mapfile:
                    vaults_map = json.loads(mapfile.read())
                    for i, vault in enumerate(vaults_map['vaults']):
                        if vault['location'] == vault_location:
                            print("Deleting {}".format(vault['id']))
                            del vaults_map['vaults'][i]
    else:
        vaults_map = None

    # if we've reached this point, we can create the vault

    vault_password = getpass.getpass(prompt="Please enter a master password: ")
    redundant_entry = getpass.getpass(prompt="Please enter password again: ")
    while vault_password != redundant_entry:
        print("Error: passwords do not match. Please try again.")
        vault_password = getpass.getpass(prompt="Please enter a master password: ")
        redundant_entry = getpass.getpass(prompt="Please enter password again: ")
    password_bytes = vault_password.encode('utf-8')

    vault_hash = hashlib.sha256(password_bytes).digest()
    vault_salt = os.urandom(SALT_SIZE)

    salt64 = b64encode(vault_salt)
    hash64 = b64encode(vault_hash)
    vault_id = salt64[:VAULT_ID_SIZE//2] + hash64[:VAULT_ID_SIZE//2]
    vault_id = vault_id.decode('utf-8')

    with open(vault_signature_location, 'wb') as signature_file:
        signature_file.write(salt64)
        signature_file.write(b'\n')
        signature_file.write(hash64)

    # this software keeps an internal map of vaults created (or imported)
    # within the user's configuration directory (default: ~/.config/coco-jumbo)
    vaults_map_location = "{}/vaults.json".format(DEFAULT_CONFIG_DIR)
    if not vaults_map and os.path.exists(vaults_map_location):
        with open(vaults_map_location, 'r') as existing_map:
            vaults_map = json.loads(existing_map.read())
    elif not vaults_map:
        vaults_map = {'vaults': []}
    vaults_map['vaults'].append({
        'id': vault_id,
        'location': vault_location,
        'tags': [args.tag] if args.tag else []
    })
    with open(vaults_map_location, 'w') as updated_map:
        updated_map.write(json.dumps(vaults_map))

    print("Successfully created vault with id {} in {}".format(vault_id,
                                                               vault_location))

    print("Would you like to generate a persistent encryption key? (y/n)")
    print("Hint: persistent key -> more convenient, no key -> more secure")
    answer = input()

    if 'y' not in answer:
        print("All done.")
        exit()

    key_location = "{}/id_fernet".format(vault_location)
    fernet_key = generate_fernet_key(vault_salt, password_bytes)

    with open(key_location, 'wb') as keyfile:
        keyfile.write(fernet_key)

    print("Successfully generated encryption key in new vault.")
