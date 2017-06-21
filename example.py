import dmpy.distributedmake as dm

m = dm.DistributedMake(dry_run=False, keep_going=True, num_jobs=10)

m.add("test_output_file", None, './test')
m.execute()
