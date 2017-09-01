from dmpy import DistributedMake, get_dm_arg_parser

# Pass --dry-run to command line
args = get_dm_arg_parser().parse_args()
m = DistributedMake(keep_going=True, args_object=args)

m.add("test_output_file", None, 'echo hi world')
m.execute()
