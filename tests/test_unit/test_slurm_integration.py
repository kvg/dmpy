from io import StringIO

from dmpy import DistributedMake, SchedulingEngine, DMBuilder


class TestDmpySlurmIntegration(object):
    def test_prefixes_all_recipes_with_srun(self):
        # given
        writer = StringIO()
        dm = DMBuilder(scheduler=SchedulingEngine.slurm)
        dm.add('output', 'input', 'echo hi world')

        # when
        dm.write_to_filehandle(writer)

        # then
        writer.seek(0)
        for line in writer:
            if line.startswith("\t"):
                if not line.startswith('\t@example_test'):
                    assert line.startswith("\tsrun ")
