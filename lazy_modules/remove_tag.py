import argparse

from lazy_modules.share.login_table_helpers import (
    read_login_table,
    write_login_table,
    query_table
)
from lazy_modules.share.user_input_helpers import user_modify_table

MODULE_ACTION_VERB = 'remove tag'


def remove_tag_from_field(field, tag):
    field_tags = field.split(', ')
    if field_tags == ['']:
        field_tags = []
    for i, field_tag in enumerate(field_tags):
        if field_tag == tag:
            del field_tags[i]
            break
    return ', '.join(field_tags)


def main(*args):
    parser = argparse.ArgumentParser(
        description='Remove an entry from the login table',
        prog=__file__.split("/")[-1]
    )
    parser.add_argument('tag', help='tag to remove from login entry')
    parser.add_argument('login_query', nargs='*',
                        help='run "lazy --help-queries" for help with these')
    args = parser.parse_args(args)

    table_rows = read_login_table()
    queried_rows = query_table(args.login_query, table_rows)

    def modify_single_entry(table, index):
        if args.tag in table[index][2]:
            table[index][2] = remove_tag_from_field(table[index][2], args.tag)

    def modify_multiple_entries(table):
        def modify_tags_if_match_login_query(row):
            if all([query in row for query in args.login_query]):
                row[2] = remove_tag_from_field(row[2], args.tag)

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
