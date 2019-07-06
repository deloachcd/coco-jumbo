import argparse

from lazy_modules.share.login_table_helpers import read_login_table, write_login_table
from lazy_modules.share.call_lesspass import validate_ruleset, call_lesspass


def user_input_answer(question):
    return "n" not in input(question)


def ruleset_from_user_answers(counter):
    symbols = user_input_answer("Are symbols allowed? (%!#@) [y/n] ")
    lowercase = user_input_answer("Are lowercase characters allowed? [y/n] ")
    uppercase = user_input_answer("Are uppercase characters allowed? [y/n] ")
    digits = user_input_answer("Are digits allowed (0-9) [y/n] ")
    length = input("Enter a length for this password (default: 16) ")
    length = 16 if length == "" else int(length)
    return (
        ("l" if lowercase else "") +
        ("u" if uppercase else "") +
        ("d" if digits else "") +
        ("s" if symbols else "") +
        "." + str(length) + (("." + str(counter)) if counter != 1 else "")
    )


def main(*args):
    parser = argparse.ArgumentParser(
        description="Add an entry into the login table", prog=__file__.split("/")[-1]
    )
    parser.add_argument(
        "platform",
        metavar="platform",
        nargs="?",
        help="platform for this login (e.g. spotify)",
    )
    parser.add_argument(
        "login",
        metavar="login",
        nargs="?",
        help="username/email/identifier for this login",
    )
    parser.add_argument(
        "-t", "--tags", nargs="+", help="tags to help query this login quickly"
    )
    parser.add_argument(
        "-r", "--ruleset", nargs="?", help="custom ruleset for password generation"
    )
    parser.add_argument(
        "-nc",
        "--no-confirm",
        nargs="?",
        help="don't prompt to confirm if the generated password works",
    )
    args = parser.parse_args(args)
    table_rows = read_login_table()

    platform = input("Platform: ") if not args.platform else args.platform
    login = input("Login: ") if not args.login else args.login
    tags = ", ".join(args.tags) if args.tags else ""
    password_generation_counter = 1

    if not args.ruleset:
        annoying_rules = user_input_answer(
            "Does this platform have specific password rules? (ex. no symbols) [y/n] "
        )
        if annoying_rules:
            ruleset = ruleset_from_user_answers(password_generation_counter)
        else:
            ruleset = 'luds.16'
    else:
        validate_ruleset(args.ruleset)
        ruleset = args.ruleset

    if not args.no_confirm:
        confirm = user_input_answer(
            "Would you like to ensure this login's password works,\n"
            "before adding it? [y/n] "
        )
        if confirm:
            works = False
            while not works:
                print("Try this password: ", end="")
                call_lesspass(platform, login, ruleset)
                works = user_input_answer(
                    "Did this password work? [y/n] "
                )
                if not works:
                    password_generation_counter += 1
                    ruleset = ruleset_from_user_answers(password_generation_counter)

    table_rows.append([platform, login, tags, ruleset])
    write_login_table(table_rows)
    print("Successfully wrote entry to login table.")
