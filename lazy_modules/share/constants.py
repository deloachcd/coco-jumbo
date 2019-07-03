import os

LAZY_USER_DATA_DIR = os.path.expanduser("~/.local/share/lazy")
LOGIN_TABLE_PATH = "{}/logins.csv".format(LAZY_USER_DATA_DIR)
MIRROR_PATH = "{}/mirrors".format(LAZY_USER_DATA_DIR)
