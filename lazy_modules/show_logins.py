import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    query_table,
    render_table
)


def main(*args):
    parser = argparse.ArgumentParser(
        description='Remove an entry from the login table',
        prog=__file__.split("/")[-1]
    )
    parser.add_argument('login_query', metavar='login_query', nargs='*',
                        help='run "lazy --help-queries" for help with these')
    args = parser.parse_args(args)
    table_rows = read_login_table()
    query_rows = query_table(args.login_query, table_rows)
    print(render_table(query_rows, number_rows=True))
