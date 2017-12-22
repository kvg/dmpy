import os

from dmpy import DistributedMake, get_dm_arg_parser

# Pass --dry-run to command line
args = get_dm_arg_parser().parse_args()
m = DistributedMake(args_object=args)

out_files = [os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          "test_output_file{}".format(str(file_num))) for file_num in range(3)]

m.add(out_files[1], None, "touch {} {} && sleep 5 && touch {}".format(*out_files))
m.execute()
