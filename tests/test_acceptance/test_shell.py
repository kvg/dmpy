import contextlib
import os
import io
import signal
import subprocess

from shutil import copyfile

from subprocess import check_call, check_output, DEVNULL

from os.path import realpath, join, dirname
import time

import sys

import attr

from dmpy import DistributedMake


@attr.s(slots=True)
class ShellTestDriver(object):
    dm = attr.ib()

    def run(self):
        self.dm.add('bla', None, 'echo $BASH')
        output = self.dm.execute(subprocess.Popen, popen_args={'stdout': subprocess.PIPE})
        stdout = output[0].decode('utf-8').split("\n")
        return stdout


class TestShell(object):
    def test_uses_bash_by_default(self):
        # given
        driver = ShellTestDriver(DistributedMake(run=True))

        # when
        stdout = driver.run()
        assert stdout[1] == "/bin/bash"

    def test_can_be_switched_to_sh(self):
        # given
        driver = ShellTestDriver(DistributedMake(run=True, shell='/bin/sh'))

        # when
        stdout = driver.run()

        # then
        assert stdout[1] == "/bin/sh"


class Test(object):
    def test_delete_output_on_keyboard_interrupt(self, tmpdir):
        # given
        example_name = 'example_sleep.py'
        example = tmpdir.join(example_name)
        out_files = [join(dirname(str(example)), 'test_output_file{}'.format(str(file_num))) for
                     file_num in range(3)]
        copyfile(realpath(join(dirname(__file__), example_name)), str(example))

        # when
        process = subprocess.Popen(' '.join(['python', str(example), '-r']), shell=True,
                                   env=os.environ)
        time.sleep(1)
        process.send_signal(signal.SIGINT)
        process.wait()

        # then
        assert os.path.isfile(out_files[0])
        assert not os.path.isfile(out_files[1])
        assert not os.path.isfile(out_files[2])
