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
        assert rule.recipe[1].startswith('echo') >= 0
        assert rule.recipe[1].find('qsub') >= 0
        assert rule.recipe[2].startswith('echo') >= 0
        assert rule.recipe[2].find('qsub') >= 0

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
        assert rule.recipe[1].endswith(f'qsub -sync y -cwd -V pe smp {opts["threads"]} -l h_vmem={opts["h_vmem"]}G,h_stack=32M -q {opts["queue"]} -o {target}.log.out -e {target}.log.err -N {cmds[0].split(" ")[0]}')
        assert rule.recipe[2].endswith(f'qsub -sync y -cwd -V pe smp {opts["threads"]} -l h_vmem={opts["h_vmem"]}G,h_stack=32M -q {opts["queue"]} -o {target}.log.out -e {target}.log.err -N {cmds[0].split(" ")[0]}')
