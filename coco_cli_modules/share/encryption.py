import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

from coco_cli_modules.share.constants import (
    KEY_SIZE
)


def generate_fernet_key(salt, password_bytes):
    backend = default_backend()
    keygen = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=100000,
        backend=backend,
    )
    key = base64.b64encode(keygen.derive(password_bytes))
    return key
