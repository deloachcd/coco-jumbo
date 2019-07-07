import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
    query_table,
    render_table,
)
from lazy_modules.share.user_input_helpers import user_input_answer
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
    table_rows = read_login_table()
    query_rows = query_table(args.login_query, table_rows)

    if len(query_rows) > 0:

        if len(query_rows) > 1:
            print(render_table(query_rows, number_rows=True))
            user_selection_answer = user_input_answer(
                "Which login do you want? [1-{}]".format(len(query_rows))
            )
        else:
            user_selection_answer = "1"

        if (
            user_selection_answer.isnumeric()
            and int(user_selection_answer) >= 1
            and int(user_selection_answer) <= len(query_rows)
        ):
            user_selection_row = query_rows[int(user_selection_answer) - 1]
            call_lesspass(
                user_selection_row[0],  # Platform
                user_selection_row[1],  # Login
                user_selection_row[3],  # Ruleset
                copy=args.copy,
            )
        else:
            print("Invalid selection specified. Exiting.")
            exit()
    else:
        print("No logins found for query. Exiting.")
        exit()
