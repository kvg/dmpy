from os.path import join, realpath, dirname
from subprocess import check_output
from shutil import copyfile


class TestDmpySchedulerFlag(object):
    def test_honors_slurm(self, tmpdir):
        # given
        example = tmpdir.join('example.py')
        test_file = tmpdir.join('example_test')
        copyfile(realpath(join(dirname(__file__), 'example.py')), str(example))
        copyfile(realpath(join(dirname(__file__), 'example_test')), str(test_file))

        # when
        output = check_output(['python', str(example), '--scheduler', 'slurm']).decode("utf-8")
        output = output.split("\n")

        # then
        assert output[2].startswith("srun ")
