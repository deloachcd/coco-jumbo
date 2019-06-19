import os
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import getpass

from constants import SALTSIZE, KEYSIZE
from CocoFileManager import CocoFileManager


if __name__ == "__main__":
    backend = default_backend()
    salt = os.urandom(SALTSIZE)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEYSIZE,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    master_pass = getpass.getpass(prompt="Please enter a master password: ")
    pass_bytes = master_pass.encode('utf-8')
    key = base64.urlsafe_b64encode(kdf.derive(pass_bytes))
    secret = salt + key

    coco_fm = CocoFileManager()
    secret_filename = "master.turtle"
    coco_fm.ensure_cocodir_exists()
    coco_fm.write_bytes_to_file(secret, secret_filename)
    print("Created a new secret turtle at {}/{}".format(
        coco_fm.cocodir, secret_filename
    ))
    assert secret[:SALTSIZE] == salt
    assert secret[SALTSIZE:] == key
