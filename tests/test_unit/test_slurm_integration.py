from io import StringIO

from dmpy import DistributedMake, SchedulingEngine


class TestDmpySlurmIntegration(object):
    def test_prefixes_all_recipes_with_srun(self):
        # given
        writer = StringIO()
        dm = DistributedMake(writer=writer, scheduler=SchedulingEngine.slurm)
        dm.add('output', 'input', 'echo hi world')

        # when
        dm.finalize()

        # then
        writer.seek(0)
        for line in writer:
            if line.startswith("\t"):
                if not line.startswith('\t@example_test'):
                    assert line.startswith("\tsrun ")
