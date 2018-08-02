from io import StringIO

from dmpy.distributedmake import SchedulingEngine, DMBuilder
from dmpy.testing.makefile_parser import extract_rules_from_makefile


class TestDmpySlurmIntegration(object):
    def test_work_commands_with_qsub(self):
        # given
        writer = StringIO()
        dm = DMBuilder(scheduler=SchedulingEngine.sge)
        dm.add('output', 'input', ['echo hi world', 'hi world again'], { 'h_vmem': 4, 'queue': 'default', 'threads': 4 })

        # when
        dm.write_to_filehandle(writer)

        # then
        rules = extract_rules_from_makefile(writer.getvalue().split("\n"))

        rule = rules[0]

        assert len(rule.recipe) == 3
        assert rule.recipe[0].startswith('@test ')
        assert rule.recipe[1].startswith('echo')
        assert 'qsub' in rule.recipe[1]
        assert rule.recipe[2].startswith('echo')
        assert 'qsub' in rule.recipe[2]

    def test_work_commands_with_qsub_args(self):
        # given
        writer = StringIO()
        test_scheduler_args = ['fries', 'and', 'cats']

        opts = { 'h_vmem': 4, 'queue': 'default', 'threads': 4 }
        target = 'output'
        source = 'input'
        cmds = ['echo hi world', 'hi world again']

        dm = DMBuilder(scheduler=SchedulingEngine.sge, scheduler_args=test_scheduler_args)
        dm.add(target, source, cmds, opts)

        # when
        dm.write_to_filehandle(writer)

        # then
        rules = extract_rules_from_makefile(writer.getvalue().split("\n"))
        rule = rules[0]
        assert len(rule.recipe) == 3
        assert rule.recipe[0].startswith('@test ')

        for arg in ['-sync y', '-cwd', '-V', f'-pe smp {opts["threads"]}', f'-l h_vmem={opts["h_vmem"]}G,h_stack=32M', f'-q {opts["queue"]}', f'-o {target}.log.out', f'-e {target}.log.err', f'-N {cmds[0].split(" ")[0]}']:
            assert arg in rule.recipe[1]
            assert arg in rule.recipe[2]
