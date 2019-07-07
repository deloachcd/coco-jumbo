import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
)
from lazy_modules.share.user_input_helpers import user_query_and_modify_table


module_action_verb = 'delete'


def modify_single_entry(table, index):
    del table[index]


def modify_multiple_entries(table, login_query):
    table = list(
        filter(
            lambda row: not all([query in row for query in login_query]),
            table
        )
    )


def main(*args):
    parser = argparse.ArgumentParser(
        description='Remove an entry from the login table',
        prog=__file__.split("/")[-1]
    )
    parser.add_argument('login_query', nargs='*',
                        help='run "lazy --help-queries" for help with these')
    args = parser.parse_args(args)

    table_rows = read_login_table()
    user_query_and_modify_table(
        table_rows,
        args.login_query,
        module_action_verb,
        modify_single_entry,
        modify_multiple_entries,
        prompt_for_confirmation=True
    )
    write_login_table(table_rows)
