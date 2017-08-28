import argparse
import os
import tempfile

from copy import copy
from subprocess import call


def add_dm_args_to_argparse_object(object):
    object.add_argument("-r", "--run", action="store_true")
    object.add_argument("-j", "--jobs", type=int, default=1)
    object.add_argument("-c", "--no-cleanup", action="store_true")
    return object


def get_dm_arg_parser(description="dmpy powered analysis"):
    parser = argparse.ArgumentParser(description=description)
    parser = add_dm_args_to_argparse_object(parser)
    return parser


class DistributedMake(object):
    def __init__(self, run=False, keep_going=False, jobs=1, no_cleanup=False, question=False,
                 touch=False, debug=False, args_object=None, writer=None, use_slurm=False):
        self.dry_run = not getattr(args_object, "run", run)
        self.keep_going = keep_going
        self.jobs = getattr(args_object, "jobs", jobs)
        self.cleanup = not getattr(args_object, 'no_cleanup', no_cleanup)
        self.question = question
        self.touch = touch
        self.debug = debug
        self.use_slurm = use_slurm

        _, self._makefile_fp = tempfile.mkstemp()
        if writer is None:
            self._writer = open(self._makefile_fp, 'w')
        else:
            self._writer = writer
        self._targets = set()
        self._targets_ordered = []
        self._write_makefile_preamble()

    @property
    def targets(self):
        return copy(self._targets_ordered)

    def _write_makefile_preamble(self):
        self._writer.write("SHELL := /bin/bash\n")

    def add(self, target, deps, cmds):
        if isinstance(cmds, str):
            cmds = [cmds]
        else:
            cmds = list(cmds)

        if isinstance(deps, str):
            deps = [deps]
        elif deps is None:
            deps = list()
        else:
            deps = list(deps)

        dirname = os.path.abspath(os.path.dirname(target))

        cmds.insert(0, "@test -d {0} || mkdir -p {0}".format(dirname))

        self._writer.write("{}: {}\n".format(target, ' '.join(deps)))
        if self.use_slurm:
            cmd_prefix = 'srun '
        else:
            cmd_prefix = ''
        for cmd in cmds:
            self._writer.write("\t{}{}\n".format(cmd_prefix, cmd))

        if target in self._targets:
            raise Exception("Tried to add target twice: {}".format(target))
        self._targets.add(target)
        self._targets_ordered.append(target)

        return

    def execute(self):
        self.finalize()
        self._writer.close()

        makecmd = []
        makecmd.append("make")

        if self.dry_run:
            makecmd.append("-n")
        if self.keep_going:
            makecmd.append("-k")
        if self.question:
            makecmd.append("-q {}".format(self.question))
        if self.touch:
            makecmd.append("-t {}".format(self.touch))
        if self.debug:
            makecmd.append("-d {}".format(self.debug))

        makecmd.append("-j {}".format(self.jobs))
        makecmd.append("-f {}".format(self._makefile_fp))
        makecmd.append("all")

        print(" ".join(makecmd))
        return_code = call(" ".join(makecmd), shell=True)
        print(" ".join(makecmd))

        if self.cleanup:
            os.remove(self._makefile_fp)

        return return_code

    def finalize(self):
        self._writer.write("all: {}\n".format(" ".join(self._targets_ordered)))
        self._writer.write(".DELETE_ON_ERROR:\n")
        self._writer.flush()
