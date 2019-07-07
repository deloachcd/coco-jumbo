import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
    query_table
)
from lazy_modules.share.user_input_helpers import user_modify_table

MODULE_ACTION_VERB = 'delete'


def main(*args):
    parser = argparse.ArgumentParser(
        description='Remove an entry from the login table',
        prog=__file__.split("/")[-1]
    )
    parser.add_argument('login_query', nargs='*',
                        help='run "lazy --help-queries" for help with these')
    args = parser.parse_args(args)
    table_rows = read_login_table()
    queried_rows = query_table(args.login_query, table_rows)

    def modify_single_entry(table, index):
        del table[index]

    def modify_multiple_entries(table):
        return list(
            filter(
                lambda row: not all([query in row for query in args.login_query]),
                table
            )
        )

    table_rows = user_modify_table(
        table_rows,
        queried_rows,
        MODULE_ACTION_VERB,
        modify_single_entry,
        modify_multiple_entries,
        prompt_for_confirmation=True
    )
    write_login_table(table_rows)
