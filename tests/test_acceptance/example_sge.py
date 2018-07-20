from pathlib import Path

from dmpy import DistributedMake, get_dm_arg_parser

# Pass --dry-run to command line
test_args = ['--scheduler', 'sge']
args = get_dm_arg_parser().parse_args(test_args)
m = DistributedMake(args_object=args)

target = Path(__file__).with_name("test_output_file").absolute()

m.add(target, None, "echo 'hi world'", { 'h_vmem': 4, 'queue': 'default', 'threads': 4 })
m.execute()
