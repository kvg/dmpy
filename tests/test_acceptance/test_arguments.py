from os.path import join, realpath, dirname
from pathlib import Path
from subprocess import check_output
from shutil import copyfile

import pytest

from dmpy.testing.makefile_parser import extract_rules_from_makefile


@pytest.fixture
def example_script(tmpdir):
    example = tmpdir.join('example.py')
    copyfile(str((Path(__file__).parent / 'example.py').absolute()), str(example))
    return example


class TestSchedulerFlag(object):
    def test_honors_slurm(self, example_script):
        # when
        output = check_output(['python', str(example_script), '--scheduler', 'slurm']).decode(
            "utf-8")
        output = output.split("\n")

        # then
        assert output[1].startswith("srun ")

    def test_honors_scheduler_args_flag(self, example_script):
        # given
        test_scheduler_args = 'test scheduler args'

        # when
        output = check_output(
            ['python', str(example_script), '--scheduler', 'slurm', '--scheduler-args',
             test_scheduler_args]).decode("utf-8")
        output = output.split("\n")

        # then
        assert test_scheduler_args in output[1]

    def test_sets_job_name(self, example_script):
        # when
        output = check_output(
            ['python', str(example_script), '--scheduler', 'slurm', '--scheduler-args',
             'arg1']).decode("utf-8")
        output = output.split("\n")

        # then
        assert '--job-name echo' in output[1]

    def test_runs_all_commands_in_bash_string(self, example_script):
        # when
        output = check_output(['python', str(example_script), '--scheduler', 'slurm']).decode(
            "utf-8")
        output = output.split("\n")

        # then
        assert output[1].endswith(" bash -c 'echo '\"'\"'hi world'\"'\"''")


class TestTouch(object):
    def test_creates_empty_result(self, example_script):
        # given
        output_file = Path(example_script).with_name('test_output_file')
        assert not output_file.exists()

        # when
        output = check_output(['python', str(example_script), '--touch']).decode("utf-8")
        # print(output)

        # then
        assert output_file.exists()
        assert output_file.stat().st_size == 0
