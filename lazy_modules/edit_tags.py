import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
    query_table
)
from lazy_modules.share.user_input_helpers import user_modify_table

MODULE_ACTION_VERB = 'edit tags'


def standardize_tags(tags):
    if isinstance(tags, str):
        tags = tags.replace(',', ' ')
        tags = ', '.join(tags.split())
    elif isinstance(tags, list):
        tags = ', '.join(tags)
    else:
        raise TypeError("'tags' must be str or list")
    return tags


def get_tags_from_user_input():
    return input("Enter new tags for this entry: ")


def main(*args):
    parser = argparse.ArgumentParser(
        description='Remove an entry from the login table',
        prog=__file__.split("/")[-1]
    )
    parser.add_argument('login_query', nargs='*',
                        help='run "lazy --help-queries" for help with these')
    parser.add_argument('-t', '--tags', nargs='+',
                        help='tags to write to login entry')
    args = parser.parse_args(args)

    table_rows = read_login_table()
    queried_rows = query_table(args.login_query, table_rows)

    tags = args.tags if args.tags else get_tags_from_user_input()
    tags = standardize_tags(tags)

    def modify_single_entry(table, index):
        table[index][2] = tags

    def modify_multiple_entries(table):
        def modify_tags_if_match_login_query(row):
            if all([query in row for query in args.login_query]):
                row[2] = tags

        return list(
            map(
                modify_tags_if_match_login_query, table
            )
        )

    table_rows = user_modify_table(
        table_rows,
        queried_rows,
        MODULE_ACTION_VERB,
        modify_single_entry,
        modify_multiple_entries
    )
    write_login_table(table_rows)
