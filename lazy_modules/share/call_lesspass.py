import re

from lesspass import core

ruleset_validity_rgx = r'^l?u?d?s?\.[1-9][0-9]?\.?[1-9]?[0-9]*'


class RulesetExpansionError(Exception):
    pass


def validate_ruleset(ruleset):
    if re.match(ruleset_validity_rgx, ruleset):
        pass
    else:
        raise RulesetExpansionError(
            "invalid password generation ruleset {}".format(
                ruleset
            )
        )


def call_lesspass(site, login, ruleset):
    def expand_ruleset(rulestr):
        validate_ruleset(rulestr)
        sections = rulestr.split('.')
        if len(sections) == 3:
            # specific counter value included
            char_inclusion_args, length, counter = sections
            if counter == "":
                # account for accepting an extra dot
                counter = '1'
        elif len(sections) == 2:
            # default to counter = 1
            char_inclusion_args, length = sections
            counter = '1'
        return (
            '-{}'.format(char_inclusion_args),
            '-L', length,
            '-C', counter
        )

    LESSPASS_ARGS = [
        site,
        login,
        *expand_ruleset(ruleset)
    ]
    core.main(LESSPASS_ARGS)


if __name__ == "__main__":
    # more convenient to eyeball the output of these test cases, as we don't
    # have to capture stdout to refactor their results into assertions
    import os
    os.environ["LESSPASS_MASTER_PASSWORD"] = "test_password"
    # first three lines of output should be the same
    call_lesspass("site.com", "example_username", "luds.16")
    call_lesspass("site.com", "example_username", "luds.16.1")
    call_lesspass("site.com", "example_username", "luds.16.")
    # this line should be different
    call_lesspass("site.com", "example_username", "luds.16.20")
    from unittest import TestCase
    t = TestCase()
    with t.assertRaises(RulesetExpansionError):
        call_lesspass("site.com", "example_username", "sud.300")
