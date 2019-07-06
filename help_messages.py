help_messsage = '''usage: {} [-hl] ( lazy_module [module_args] ) | lazy_query

The lazy man's command line login manager for LessPass.

positional arguments (module execution):
  lazy_module  module to run (--list-modules to see all)
  module_args  arguments to pass to the selected module (if necessary)

positional arguments (login retrieval query):
  lazy_query   query to access and retrieve login info with

optional arguments:
  -h, --help           show this help message and exit
  -l, --list-modules   display all possible options for coco-module
  --help-queries       display help with writing login queries
'''.format(
      __file__
  )
help_queries = '''
Login queries are what you use to retrieve login info quickly.

Let's say your login table looks like this:
| # | Platform           | Login          | Tags   | Ruleset |
|---+--------------------+----------------+--------+---------|
| 0 | google             | example        |        | luds.16 |
| 1 | linkedin           | shocklord_666  | career | luds.16 |
| 2 | youtube            | other_example  | google | luds.16 |
| 2 | mildewfanatics.com | mildew_man_183 | dew    | luds.16 |
| 3 | geekforums.net     | the_googler    |        | luds.16 |

A query for 'google' will give you this result:
| # | Platform           | Login          | Tags   | Ruleset |
|---+--------------------+----------------+--------+---------|
| 0 | google             | example        |        | luds.16 |
| 1 | youtube            | other_example  | google | luds.16 |
| 2 | geekforums.net     | the_googler    |        | luds.16 |

A query for 'google example' will give you this result:
| # | Platform           | Login          | Tags   | Ruleset |
|---+--------------------+----------------+--------+---------|
| 0 | google             | example        |        | luds.16 |
| 1 | youtube            | other_example  | google | luds.16 |

You can use these queries with all modules except 'add-login'
(because it doesn't really need it)
'''
