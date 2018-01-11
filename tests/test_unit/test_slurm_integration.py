from io import StringIO

from dmpy.distributedmake import SchedulingEngine, DMBuilder
from dmpy.testing.makefile_parser import extract_rules_from_makefile


class TestDmpySlurmIntegration(object):
    def test_prefixes_work_commands_with_srun(self):
        # given
        writer = StringIO()
        dm = DMBuilder(scheduler=SchedulingEngine.slurm)
        dm.add('output', 'input', ['echo hi world', 'hi world again'])

        # when
        dm.write_to_filehandle(writer)

        # then
        rules = extract_rules_from_makefile(writer.getvalue().split("\n"))
        rule = rules[0]
        assert len(rule.recipe) == 3
        assert rule.recipe[0].startswith('@test ')
        assert rule.recipe[1].startswith('srun ')
        assert rule.recipe[2].startswith('srun ')

    def test_prefixes_work_commands_with_srun_args(self):
        # given
        writer = StringIO()
        test_scheduler_args = ['fries', 'and', 'cats']
        dm = DMBuilder(scheduler=SchedulingEngine.slurm, scheduler_args=test_scheduler_args)
        dm.add('output', 'input', ['echo hi world', 'hi world again'])

        # when
        dm.write_to_filehandle(writer)

        # then
        rules = extract_rules_from_makefile(writer.getvalue().split("\n"))
        rule = rules[0]
        assert len(rule.recipe) == 3
        assert rule.recipe[0].startswith('@test ')
        assert rule.recipe[1].startswith(
            'srun --quit-on-interrupt --job-name echo {}'.format(' '.join(test_scheduler_args)))
        assert rule.recipe[2].startswith(
            'srun --quit-on-interrupt --job-name echo {}'.format(' '.join(test_scheduler_args)))
