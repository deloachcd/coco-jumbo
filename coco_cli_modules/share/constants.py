import os

SALT_SIZE = 32
KEY_SIZE = 32
VAULT_ID_SIZE = 20  # This number must be divisible by 2!
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.config/coco-jumbo")
FK_HEADER = b"--- FERNET SYMMETRIC KEY: KEEP THIS FILE SAFE! ---\n"
FK_FOOTER = b"\n--- END FERNET SYMMETRIC KEY ---\n"
