import os
import base64
import hashlib

import attr
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import getpass

from constants import SALTSIZE, KEYSIZE


@attr.s
class Turtle:
    def __init__(self):
        pass


if __name__ == "__main__":
    backend = default_backend()
    master_pass_salt = os.urandom(SALTSIZE)
    kdf1 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEYSIZE,
        salt=master_pass_salt,
        iterations=100000,
        backend=backend
    )
    kdf2 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEYSIZE,
        salt=master_pass_salt,
        iterations=100000,
        backend=backend
    )
    master_pass = getpass.getpass(prompt="Please enter a master password: ")
    master_pass_bytes = master_pass.encode('utf-8')
    h = hashlib.sha256()
    h.update(master_pass_bytes)
    master_pass_hash = h.digest()
    key1 = base64.urlsafe_b64encode(kdf1.derive(master_pass_bytes))
    key2 = base64.urlsafe_b64encode(kdf2.derive(master_pass_bytes))
    fern1 = Fernet(key1)
    fern2 = Fernet(key2)
    token1 = fern1.encrypt(master_pass_bytes)
    token2 = fern2.encrypt(master_pass_bytes)
    decrypt1 = fern1.decrypt(token2)
    decrypt2 = fern2.decrypt(token1)
    assert decrypt1 == decrypt2
