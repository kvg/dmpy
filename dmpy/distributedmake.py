import tempfile
from subprocess import call
import os


def add_dm_args_to_argparse_object(object):
    object.add_argument("-d", "--dry-run", action="store_true")
    return object


class DistributedMake():
    dry_run = True
    keep_going = False
    num_jobs = 1
    cleanup = True
    question = False
    touch = False
    debug = False

    __mfd, __mfp = tempfile.mkstemp()
    __writer = open(__mfp, 'w')
    __targets = []

    def __init__(self, dry_run=True, keep_going=False, num_jobs=1, cleanup=True, question=False,
                 touch=False, debug=False):
        self.dry_run = dry_run
        self.keep_going = keep_going
        self.num_jobs = num_jobs
        self.cleanup = cleanup
        self.question = question
        self.touch = touch
        self.debug = debug

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
