from pathlib import Path

from dmpy import DistributedMake, get_dm_arg_parser

# Pass --dry-run to command line
args = get_dm_arg_parser().parse_args()
m = DistributedMake(args_object=args)

target = Path(__file__).with_name("test_output_file").absolute()

m.add(target, None, "echo 'hi world'")
m.execute()
