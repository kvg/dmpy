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
        assert output[1].startswith("srun ")

    def test_honors_scheduler_args_flag(self, tmpdir):
        # given
        example = tmpdir.join('example.py')
        copyfile(realpath(join(dirname(__file__), 'example.py')), str(example))
        test_scheduler_args = 'test scheduler args'

        # when
        output = check_output(['python', str(example), '--scheduler', 'slurm', '--scheduler-args',
                               test_scheduler_args]).decode("utf-8")
        output = output.split("\n")

        # then
        assert test_scheduler_args in output[1]

    def test_sets_job_name(self, tmpdir):
        # given
        example = tmpdir.join('example.py')
        copyfile(realpath(join(dirname(__file__), 'example.py')), str(example))

        # when
        output = check_output(['python', str(example), '--scheduler', 'slurm', '--scheduler-args',
                               'arg1']).decode("utf-8")
        output = output.split("\n")

        # then
        assert '--job-name echo' in output[1]

    def test_runs_all_commands_in_bash_string(self, tmpdir):
        # given
        example = tmpdir.join('example.py')
        copyfile(realpath(join(dirname(__file__), 'example.py')), str(example))

        # when
        output = check_output(['python', str(example), '--scheduler', 'slurm']).decode("utf-8")
        output = output.split("\n")

        # then
        assert output[1].endswith(" bash -c 'echo '\"'\"'hi world'\"'\"''")
