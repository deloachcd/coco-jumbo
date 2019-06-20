import os
import base64

import attr
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import getpass

from constants import KEYSIZE, SALTSIZE


@attr.s
class CocoEncrypter:
    fernet_instance = attr.ib(default=None)

    @staticmethod
    def generate_key(salt, password_bytes):
        backend = default_backend()
        keygen = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEYSIZE,
            salt=salt,
            iterations=100000,
            backend=backend,
        )
        key = base64.urlsafe_b64encode(keygen.derive(password_bytes))
        return key

    @classmethod
    def from_key(cls, key):
        return cls(fernet_instance=Fernet(key))

    @classmethod
    def from_user_input_password(cls):
        salt = os.urandom(SALTSIZE)
        master_pass = getpass.getpass(prompt="Please enter a master password: ")
        key = cls.generate_key(salt, master_pass)
        return cls(fernet_instance=Fernet(key))
