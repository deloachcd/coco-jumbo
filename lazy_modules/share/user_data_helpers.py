import csv
import os
from pathlib import Path

from constants import (
    LAZY_USER_DATA_DIR,
    LOGIN_TABLE_PATH,
    MIRROR_PATH
)
from tables import DisplayTable


def _ensure_user_data_files_exist():
    if not os.path.isdir(LAZY_USER_DATA_DIR):
        os.makedirs(LAZY_USER_DATA_DIR)
    if not os.path.exists(LOGIN_TABLE_PATH):
        Path(LOGIN_TABLE_PATH).touch()
    if not os.path.exists(MIRROR_PATH):
        Path(MIRROR_PATH).touch()


def print_login_table():
    _ensure_user_data_files_exist()
    with open(LOGIN_TABLE_PATH, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        table = DisplayTable.from_2d_array(list(reader))
        print(table.render())
        print(table.render(index_column=True))


def _test():
    print_login_table()


if __name__ == "__main__":
    _test()
