import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
    query_table,
    render_table
)
from lazy_modules.share.user_input_helpers import user_input_answer


def main(*args):
    parser = argparse.ArgumentParser(
        description='Remove an entry from the login table',
        prog=__file__.split("/")[-1]
    )
    parser.add_argument('login_query', nargs='*',
                        help='run "lazy --help-queries" for help with these')
    args = parser.parse_args(args)
    table_rows = read_login_table()
    query_rows = query_table(args.login_query, table_rows)

    if len(query_rows) > 0:
        print(render_table(query_rows, number_rows=True))
        user_deletion_answer = user_input_answer(
            "Which entry would you like to remove? [1-{}, or '*' for all]".format(
                len(query_rows)
            )
        )
        if user_deletion_answer == '*':
            # delete all rows matched by the query
            if user_input_answer(
                    "Do you really want to delete all {} records?".format(
                        len(query_rows))
            ):
                pass

