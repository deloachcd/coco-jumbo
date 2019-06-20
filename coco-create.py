import os
import hashlib

import getpass
import colorama

from constants import (
    SALTSIZE,
    DEFAULT_COCODIR,
    DEFAULT_SECRET_FILENAME
)
from CocoEncrypter import CocoEncrypter
from CocoLocalSecret import CocoLocalSecret

DEBUG = False  # Remove this before initial release

if __name__ == "__main__":
    salt = os.urandom(SALTSIZE)
    master_pass = getpass.getpass(prompt="Please enter a master password: ")
    pass_bytes = master_pass.encode("utf-8")
    key = CocoEncrypter.generate_key(salt, pass_bytes)
    master_hash = hashlib.sha256(pass_bytes).digest()
    secret = salt + key + master_hash

    local_secret_path = "{}/{}".format(DEFAULT_COCODIR,
                                       DEFAULT_SECRET_FILENAME)
    if not os.path.exists(DEFAULT_COCODIR):
        os.makedirs(DEFAULT_COCODIR)
    if os.path.exists(local_secret_path):
        if "y" not in (
            input(
                "Local secret exists at {}\nOverwrite it? (y/n) ".format(
                    local_secret_path
                )
            ).lower()
        ):
            print("Aborting.")
            exit()
    coco_secret = CocoLocalSecret(path=local_secret_path)
    coco_secret.write_to_filesystem(secret)
    print(
        "Created a new local secret at {}\n"
        "{}Keep this file {}safe{}, and {}don't{} share it with anyone!"
        "{}".format(
            local_secret_path,
            colorama.Style.BRIGHT,
            colorama.Fore.GREEN,
            colorama.Fore.RESET,
            colorama.Fore.RED,
            colorama.Fore.RESET,
            colorama.Style.RESET_ALL,
        )
    )
    if DEBUG:
        # Make these their own unit test cases before initial release
        coco_secret.load_secret_from_filesystem()
        assert coco_secret.has_secret_at_path()
        assert key == coco_secret.get_key()
        assert salt == coco_secret.get_salt()
        assert master_hash == coco_secret.get_hash()
