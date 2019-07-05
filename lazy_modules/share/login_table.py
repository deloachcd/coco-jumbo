import csv
import os
import pathlib
import random

from constants import LAZY_USER_DATA_DIR, LOGIN_TABLE_PATH, DISPLAYTABLE_HEADER
from tables import DisplayTable


class InvalidFieldNameException(Exception):
    pass


# testing functions
def generate_random_word():
    return "".join([chr(random.randrange(97, 123)) for i in range(10)])


def _get_login_table_csv(mode):
    if not os.path.isdir(LAZY_USER_DATA_DIR):
        os.makedirs(LAZY_USER_DATA_DIR)
    if not os.path.exists(LOGIN_TABLE_PATH):
        pathlib.Path(LOGIN_TABLE_PATH).touch()
    return open(LOGIN_TABLE_PATH, mode, newline="")


def _read_login_table():
    with _get_login_table_csv("r") as csvfile:
        return list(csv.reader(csvfile, delimiter=",", quotechar='"'))


def _write_login_table(table):
    with _get_login_table_csv("w") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        for row in table:
            writer.writerow(row)


def _single_query_table(query, table):
    queried_rows = []
    for i, row in enumerate(table):
        if query in "|".join(row[:3]):
            queried_row = row
            queried_row.append(i)
            queried_rows.append(queried_row)
    return queried_rows


def query_table(query_tokens, table):
    """This function takes a set of query tokens, and returns a list of
    all rows which contain every token (token_1 OR token_2 OR ... token_n)

    Time complexity: O(q*n), q = num queries, n = records in login table"""
    queried_rows = table
    for token in query_tokens:
        # reduce table iteratively by running each query after
        # the first on results of last query
        queried_rows = _single_query_table(token, queried_rows)
    return queried_rows


def query_login_table(query_tokens):
    return query_table(query_tokens, _read_login_table())


def render_table(table, **kwargs):
    renderable = DisplayTable.from_2d_array([DISPLAYTABLE_HEADER] + table)
    return renderable.render(**kwargs)


def render_login_table(**kwargs):
    return render_table(_read_login_table(), **kwargs)


def get_login_table_index(query_row):
    return query_row[-1] + 1


def get_table_row_content(table, row_number, field_name):
    field_names = [field.lower() for field in DISPLAYTABLE_HEADER]
    if field_name in field_names:
        return table[row_number - 1][field_names.index(field_name)]
    else:
        raise InvalidFieldNameException(
            "'{}' is not a valid field name.".format(field_name)
        )


def get_table_row_content_query_row(table, query_row, field_name):
    return get_table_row_content(table, get_login_table_index(query_row), field_name)


def _test():
    selected_row = 2
    rows, queries = [], []
    for i in range(10):
        platform, login = generate_random_word(), generate_random_word()
        rows.append([platform, login, ", ".join([]), "luds.16"])
        if i == selected_row:
            queries.append(platform[4:])
    print(render_table(rows, number_rows=True))
    queried_table = query_table(queries, rows)
    print(render_table(queried_table, number_rows=True))
    print(get_table_row_content_query_row(rows, queried_table[0], 'ruleset'))
    print(get_table_row_content_query_row(rows, queried_table[0], 'platform'))
    print(get_table_row_content_query_row(rows, queried_table[0], 'login'))


if __name__ == "__main__":
    _test()
