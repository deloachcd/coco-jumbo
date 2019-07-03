import re

from lazy_modules.share import call_lesspass


def test_ruleset_validation_regex():
    ruleset_rgx = call_lesspass.ruleset_validity_rgx
    assert re.match(ruleset_rgx, 'luds.16')
    assert not re.match(ruleset_rgx, 'luds.06')
    assert re.match(ruleset_rgx, 'luds.16.32')
    assert re.match(ruleset_rgx, 'luds.16.')
    assert not re.match(ruleset_rgx, 'llds.16')
    assert not re.match(ruleset_rgx, 'luds')
