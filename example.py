from dmpy.distributedmake import DistributedMake, get_dm_arg_parser

# Pass --dry-run to command line
args = get_dm_arg_parser().parse_args()
m = DistributedMake(dry_run=False, keep_going=True, num_jobs=10, args_object=args)

m.add("test_output_file", None, './test')
m.execute()
