import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    query_table,
    render_table
)


def main(*args):
    parser = argparse.ArgumentParser(
        description=None
    )
    # change to display correct program name on parsing error, even though we
    # call this main procedure from another module (coco-cli.py)
    parser.prog = __file__.split("/")[-1]
    args = parser.parse_args(args)
