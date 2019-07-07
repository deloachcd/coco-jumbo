import csv
import os
import pathlib
import random

from lazy_modules.share.constants import (
    LAZY_USER_DATA_DIR,
    LOGIN_TABLE_PATH,
    DISPLAYTABLE_HEADER
)
from lazy_modules.share.tables import DisplayTable


class InvalidFieldNameException(Exception):
    pass


# constants we only need in this file
FIELD_NAMES = [field.lower() for field in DISPLAYTABLE_HEADER]


# testing functions
# TODO: put this somewhere else
def generate_random_word():
    return "".join([chr(random.randrange(97, 123)) for i in range(10)])


def _get_login_table_csv(mode):
    return open(LOGIN_TABLE_PATH, mode, newline="")


def read_login_table(tags_as_list=False):
    # ensure the file exists
    if not os.path.isdir(LAZY_USER_DATA_DIR):
        os.makedirs(LAZY_USER_DATA_DIR)
    if not os.path.exists(LOGIN_TABLE_PATH):
        pathlib.Path(LOGIN_TABLE_PATH).touch()
    # now we can safely open it
    with _get_login_table_csv("r") as csvfile:
        table_rows = list(csv.reader(csvfile, delimiter=",", quotechar='"'))
        return table_rows


def write_login_table(table):
    with _get_login_table_csv("w") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for row in table:
            writer.writerow(row)


def query_table(query_tokens, table):
    """This function takes a set of query tokens, and returns a list of
    all rows which contain every token (token_1 OR token_2 OR ... token_n)

    Time complexity: O(q*n), q = num queries, n = records in login table"""

    def query_reduce(query, table):
        queried_rows = []
        for i, row in enumerate(table):
            if query in "|".join(row[:3]):
                queried_row = row
                queried_row.append(i)
                queried_rows.append(queried_row)
        return queried_rows

    queried_rows = table
    if isinstance(query_tokens, list):
        for token in query_tokens:
            # reduce table iteratively by running each query after
            # the first on results of last query
            queried_rows = query_reduce(token, queried_rows)
    elif isinstance(query_tokens, str):
        queried_rows = query_reduce(query_tokens, queried_rows)
    elif query_tokens is None:
        pass
    else:
        raise TypeError(
            "Invalid type '{}' for 'query_tokens' parameter".format(
                type(query_tokens).__name__
            )
        )
    return queried_rows


def render_table(table, **kwargs):
    renderable = DisplayTable.from_2d_array([DISPLAYTABLE_HEADER] + table)
    return renderable.render(**kwargs)


def get_queried_row_index(queried_row):
    return queried_row[-1]


def get_row_content(table, row_index, field_name):
    if field_name in FIELD_NAMES:
        return table[row_index][FIELD_NAMES.index(field_name)]
    else:
        raise InvalidFieldNameException(
            "'{}' is not a valid field name.".format(field_name)
        )


def get_index_in_table(queried_row):
    return queried_row[-1] + 1
