import argparse
import json
import os

from coco_cli_modules.share.vaults import (
    get_vault_id,
    get_vault_location,
    get_vault_tags,
    vault_has_key,
)
from coco_cli_modules.share.tables import DisplayTable
from coco_cli_modules.share.constants import DEFAULT_CONFIG_DIR


def stringify_logic(s):
    if isinstance(s, type(None)) or s == []:
        return "n/a"
    elif isinstance(s, bool):
        return "yes" if s else "no"
    elif isinstance(s, list):
        return ", ".join(s)
    else:
        return str(s)


def main(*args):
    parser = argparse.ArgumentParser(description=None)
    # change to display correct program name on parsing error, even though we
    # call this main procedure from another module (coco-cli.py)
    parser.prog = __file__.split("/")[-1]
    args = parser.parse_args(args)

    vault_map_location = "{}/vaults.json".format(DEFAULT_CONFIG_DIR)
    if not os.path.exists(vault_map_location):
        # TODO: implement autoregeneration via 'find ~ | grep .cocojumbo'
        print("Error: no 'vaults.json' file found in {}".format(DEFAULT_CONFIG_DIR))
        exit()
    else:
        with open(vault_map_location, "r") as mapfile:
            vault_map = json.loads(mapfile.read())

    table = DisplayTable(
        {
            "Tags": get_vault_tags,
            "Location": get_vault_location,
            "Has key?": vault_has_key,
            "Vault ID": get_vault_id,
        },
        vault_map["vaults"],
        stringify=stringify_logic,
    )
    print(table.render())
