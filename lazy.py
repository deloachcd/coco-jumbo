from importlib import import_module
import os
import sys

from getpass import getpass

from help_messages import (
    help_messsage,
    help_queries
)

modules_location = 'lazy_modules'
alias_modules = {
    # NOTE: alias for 'lazy get-login' is just 'lazy'
    'al': 'add-login',
    'at': 'add-tag',
    'rl': 'remove-login',
    'rt': 'remove-tag',
    'ep': 'edit-platform',
    'eu': 'edit-username',
    'et': 'edit-tags',
    'sl': 'show-logins',
}
module_aliases = alias_modules.keys()
possible_modules = alias_modules.values()


def main(args=sys.argv):
    module_to_execute = None

    # help message argument switching
    if len(args) < 2:
        module_to_execute = 'get-login'
    elif args[1] == '-h' or args[1] == '--help':
        print(help_messsage)
        exit()
    elif args[1] == '-l' or args[1] == '--list-modules':
        print("Valid options for lazy-module include:")
        for module in possible_modules:
            print("    {}".format(module))
        exit()
    elif args[1] == '--help-queries':
        print(help_queries)
        exit()

    if 'LESSPASS_MASTER_PASSWORD' not in os.environ.keys():
        os.environ['LESSPASS_MASTER_PASSWORD'] = getpass("Master password: ")

    if len(args) > 1:
        user_module = args[1]
        arg_index = 2
        if user_module in module_aliases:
            module_to_execute = alias_modules[user_module]
        elif user_module in possible_modules:
            module_to_execute = user_module
        else:
            module_to_execute = 'get-login'
            arg_index = 1

    # by this point, we know the user got the syntax right
    module_to_execute = module_to_execute.replace('-', '_')
    mod = import_module('{}.{}'.format(modules_location, module_to_execute))

    mod.main(*args[arg_index:])


if __name__ == "__main__":
    main()
