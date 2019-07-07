import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
    query_table,
    query_in_row,
    get_queried_row_index,
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

    print(render_table(query_rows, number_rows=True))
    user_deletion_answer = input(
        "Which entry would you like to remove? [1-{}, or '*' for all] ".format(
            len(query_rows)
        )
    )

    if user_deletion_answer == '*':
        # delete all rows matched by the query
        if user_input_answer(
                "Do you really want to delete all {} records? [y/n] ".format(
                    len(query_rows))
        ):
            table_rows = filter(
                lambda row: not all([query in row for query in args.login_query]),
                table_rows
            )
            table_rows = list(table_rows)
        else:
            print("Exiting.")
            exit()
    elif (
            user_deletion_answer.isnumeric() and
            int(user_deletion_answer) >= 1 and
            int(user_deletion_answer) <= len(query_rows)
    ):
        deletion_index = int(user_deletion_answer)-1
        queried_row = query_rows[deletion_index]
        del table_rows[get_queried_row_index(queried_row)]
    else:
        print("Invalid entry specified for deletion, exiting.")
        exit()

    write_login_table(table_rows)
