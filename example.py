import dmpy.distributedmake as dm

m = dm.DistributedMake(dryRun=False, keepGoing=True, numJobs=10)

m.add("test_output_file", None, './test')
m.execute()
