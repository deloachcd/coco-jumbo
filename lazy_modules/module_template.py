import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
    query_table,
    render_table
)


def main(*args):
    parser = argparse.ArgumentParser(
        description=None
    )
    parser.add_argument('login_query', metavar='login_query', nargs='?',
                        help='run "lazy --help-queries" for help with these')
    # change to display correct program name on parsing error, even though we
    # call this main procedure from another module (coco-cli.py)
    parser.prog = __file__.split("/")[-1]
    args = parser.parse_args(args)
