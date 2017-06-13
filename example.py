import distributedmake as dm

m = dm.DistributedMake(dryRun=False, keepGoing=True, numJobs=10)

m.add('./test', target='test')
m.execute()

