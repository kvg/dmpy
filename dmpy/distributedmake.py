import argparse
import tempfile
from subprocess import call
import os


def add_dm_args_to_argparse_object(object):
    object.add_argument("-r", "--no-dry-run", action="store_true")
    object.add_argument("-n", "--num-jobs", type=int, default=1)
    object.add_argument("-c", "--no-cleanup", action="store_true")
    return object


def get_dm_arg_parser(description="dmpy powered analysis"):
    parser = argparse.ArgumentParser(description=description)
    parser = add_dm_args_to_argparse_object(parser)
    return parser


class DistributedMake(object):
    def __init__(self, no_dry_run=False, keep_going=False, num_jobs=1, no_cleanup=False, question=False,
                 touch=False, debug=False, args_object=None):
        self.dry_run = not getattr(args_object, "no_dry_run", no_dry_run)
        self.keep_going = keep_going
        self.num_jobs = getattr(args_object, "num_jobs", num_jobs)
        self.cleanup = not getattr(args_object, 'no_cleanup', no_cleanup)
        self.question = question
        self.touch = touch
        self.debug = debug

        self.__mfd, self.__mfp = tempfile.mkstemp()
        self.__writer = open(self.__mfp, 'w')
        self.__targets = []
        self._write_makefile_preamble()

    def _write_makefile_preamble(self):
        self.__writer.write("SHELL := /bin/bash\n")

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

        self.__writer.write("{}: {}\n".format(target, ' '.join(deps)))
        self.__writer.write("\t{}\n".format("\n\t".join(cmds)))

        self.__targets.append(target)

        return

    def execute(self):
        self.__writer.write("all: {}\n".format(" ".join(self.__targets)))
        self.__writer.close()

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

        makecmd.append("-j{}".format(self.num_jobs))
        makecmd.append("-f {}".format(self.__mfp))
        makecmd.append("all")

        print(" ".join(makecmd))
        return_code = call(" ".join(makecmd), shell=True)
        print(" ".join(makecmd))

        if self.cleanup:
            os.remove(self.__mfp)

        return return_code
