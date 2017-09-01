from io import StringIO

from dmpy.distributedmake import SchedulingEngine, DMBuilder
from dmpy.testing.makefile_parser import extract_rules_from_makefile


class TestDmpySlurmIntegration(object):
    def test_prefixes_expected_recipes_with_srun(self):
        # given
        writer = StringIO()
        dm = DMBuilder(scheduler=SchedulingEngine.slurm)
        dm.add('output', 'input', 'echo hi world')

        # when
        dm.write_to_filehandle(writer)

        # then
        rules = extract_rules_from_makefile(writer.getvalue().split("\n"))
        rule = rules[0]
        assert len(rule.recipe) == 2
        assert rule.recipe[0].startswith('@test ')
        assert rule.recipe[1].startswith('srun ')
