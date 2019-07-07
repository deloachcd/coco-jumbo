import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    query_table,
)
from lazy_modules.share.user_input_helpers import execute_function_on_user_selected_row
from lazy_modules.share.call_lesspass import call_lesspass


def main(*args):
    parser = argparse.ArgumentParser(
        description="retrive the password LessPass generates for a login"
    )
    parser.add_argument(
        "login_query",
        metavar="login_query",
        nargs="*",
        help='run "lazy --help-queries" for help with these',
    )
    parser.add_argument(
        "-c", "--copy", action="store_true", help="copy password to clipboard"
    )
    args = parser.parse_args(args)

    def call_lesspass_from_row(row, copy=False):
        call_lesspass(
            row[0],  # Platform
            row[1],  # Login
            row[3],  # Ruleset
            copy=args.copy
        )

    table_rows = read_login_table()
    query_rows = query_table(args.login_query, table_rows)

    execute_function_on_user_selected_row(
        query_rows,
        call_lesspass_from_row
    )
