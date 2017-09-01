import io
from contextlib import redirect_stdout, redirect_stderr

import re

from subprocess import check_call, check_output, DEVNULL

from dmpy import DistributedMake


class TestShell(object):
    def test_uses_bash_by_default(self):
        # given
        dm = DistributedMake(run=True)
        dm.add('bla', None, 'echo $BASH')

        # when
        output = dm.execute(check_output)
        output = output.decode('utf-8').split("\n")
        assert output[1] == "/bin/bash"

    def test_can_be_switched_to_sh(self):
        # given
        dm = DistributedMake(run=True, shell='/bin/sh')
        dm.add('bla', None, 'echo $BASH')

        # when
        output = dm.execute(check_output)
        output = output.decode('utf-8').split("\n")
        assert output[1] == "/bin/sh"
