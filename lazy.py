from importlib import import_module
import os
import sys

from getpass import getpass


modules_location = 'lazy_modules'
possible_modules = [
    'module_template',
    'test'
]
help_messsage = '''usage: {} [-hls] ( lazy_module [module_args] ) | lazy_query

The lazy man's command line login manager for LessPass.

positional arguments (module execution):
  lazy_module  module to run (--list-modules to see all)
  module_args  arguments to pass to the selected module (if necessary)

positional arguments (login retrieval query):
  lazy_query   query to access and retrieve login info with

optional arguments:
  -h, --help           show this help message and exit
  -l, --list-modules   display all possible options for coco-module
  -s, --store-master   store master password in environment variable
'''.format(
      __file__
  )


def main(args=sys.argv):
    if len(args) < 2 or args[1] == '-h' or args[1] == '--help':
        print(help_messsage)
        exit()
    elif args[1] == '-l' or args[1] == '--list-modules':
        print("Valid options for coco-module include:")
        for module in possible_modules:
            print("    {}".format(module))
        exit()
    elif args[1] == '-s' or args[1] == '--store-master':
        os.environ['LESSPASS_MASTER_PASSWORD'] = getpass("Master password: ")

    user_module = args[1]
    if user_module not in possible_modules:
        print("ERROR: '{}' is not a valid option for lazy-module".format(
            user_module
        ))
        print("Run '{} --list-modules' to see valid options".format(__file__))
        exit()

    # by this point, we know the user got the syntax right
    user_module = user_module.replace('-', '_')
    mod = import_module('{}.{}'.format(modules_location, user_module))

    mod.main(*args[2:])


if __name__ == "__main__":
    main()
