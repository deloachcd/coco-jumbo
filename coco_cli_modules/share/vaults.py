import os

# These functions use entries in this software's list of
# vaults in JSON format to derive info about vaults
#
# default: ~/.config/coco-jumbo/vaults.json


def get_vault_id(map_entry):
    return map_entry['id']


def get_vault_location(map_entry):
    return map_entry['location']


def get_vault_tags(map_entry):
    return map_entry['tags']


def vault_has_key(map_entry):
    return os.path.exists("{}/id_fernet".format(map_entry['location']))


def get_vault_signature_from_filesystem(vault_location):
    with open(vault_location, 'r') as vaultfile:
        lines = vaultfile.readlines()
    return lines[0].replace('\n', ''), lines[1]
