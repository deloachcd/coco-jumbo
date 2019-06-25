from importlib import import_module
import sys

possible_modules = [
    'create-vault',
    'list-vaults',
    'vault-info',
    'vault-logins',
    'create-login',
    'list-logins',
    'get-login',
    'copy-password',
    'create-key',
    'destroy-key'
]

help_messsage = '''usage: coco-cli.py [-hl] coco-module [module-args]

The Coco Jumbo command line login manager.

positional arguments:
  coco-module  module to run (--list-modules to see all)
  module_args  arguments to pass to the selected module (if necessary)

optional arguments:
  -h, --help           show this help message and exit
  -l, --list-modules   display all possible options for coco-module'''

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print(help_messsage)
        exit()
    elif sys.argv[1] == '-l' or sys.argv[1] == '--list-modules':
        print("Valid options for coco-module include:")
        for module in possible_modules:
            print("    {}".format(module))
        exit()

    user_module = sys.argv[1]
    if user_module not in possible_modules:
        print("ERROR: '{}' is not a valid option for coco-module".format(
            user_module
        ))
        print("Run 'coco-cli.py --list-modules' to see valid options")
        exit()

    # by this point, we know the user got the syntax right
    user_module = user_module.replace('-', '_')
    mod = import_module('coco_cli_modules.{}'.format(user_module))

    mod.main(*sys.argv[2:])
