import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
    query_table,
    render_table
)


def main(*args):
    parser = argparse.ArgumentParser(
        description=None,
        prog=__file__.split("/")[-1]
    )
    parser.add_argument('tag', help='tag to add to a login entry')
    parser.add_argument('login_query', nargs='*',
                        help='run "lazy --help-queries" for help with these')
    args = parser.parse_args(args)
    table_rows = read_login_table()
    query_rows = query_table(args.login_query, table_rows)

    if len(query_rows) > 1:
        print(render_table(query_rows, number_rows=True))
        user_selection_answer = input(
            "Which entry would you like to tag? [1-{}, or '*' for all] ".format(
                len(query_rows)
            )
        )
    else:
        user_selection_answer = '1'
