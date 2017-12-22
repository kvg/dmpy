from os.path import join, realpath, dirname
from subprocess import check_output
from shutil import copyfile

from dmpy.testing.makefile_parser import extract_rules_from_makefile


class TestDmpySchedulerFlag(object):
    def test_honors_slurm(self, tmpdir):
        # given
        example = tmpdir.join('example.py')
        copyfile(realpath(join(dirname(__file__), 'example.py')), str(example))

        # when
        output = check_output(['python', str(example), '--scheduler', 'slurm']).decode("utf-8")
        output = output.split("\n")

        # then
        assert output[2].startswith("srun ")

    def test_honors_scheduler_args_flag(self, tmpdir):
        # given
        example = tmpdir.join('example.py')
        copyfile(realpath(join(dirname(__file__), 'example.py')), str(example))

        # when
        output = check_output(['python', str(example), '--scheduler', 'slurm', '--scheduler-args',
                               'hi slurm']).decode("utf-8")
        output = output.split("\n")

        # then
        assert output[2].startswith("srun --quit-on-interrupt hi slurm ")

    def test_runs_all_commands_in_bash_string(self, tmpdir):
        # given
        example = tmpdir.join('example.py')
        copyfile(realpath(join(dirname(__file__), 'example.py')), str(example))

        # when
        output = check_output(['python', str(example), '--scheduler', 'slurm']).decode("utf-8")
        output = output.split("\n")

        # then
        assert output[2].endswith(" bash -c 'echo '\"'\"'hi world'\"'\"''")
