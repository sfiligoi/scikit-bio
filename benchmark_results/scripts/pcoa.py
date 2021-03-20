import sys
import h5py
import skbio

import time

t1=time.time()
with h5py.File(sys,argv[2],"r") as f_u:
 dm_u=skbio.stats.distance.DistanceMatrix(f_u['matrix'][:,:],f_u['order'][:])

t2=time.time()
print("=== %s FileLoad time: %.2f"%(sys.argv[1], t2-t1))

t1=time.time()
pc = skbio.stats.ordination.pcoa(dm_u, method='fsvd', number_of_dimensions=5)
t2=time.time()
print("=== %s PCOA=5 time:  %.2f"%(sys.argv[1], t2-t1))
print(pc)

t1=time.time()
pc = skbio.stats.ordination.pcoa(dm_u, method='fsvd', number_of_dimensions=10)
t2=time.time()
print("=== %s PCOA=10 time:  %.2f"%(sys.argv[1], t2-t1))
print(pc)

t1=time.time()
pc = skbio.stats.ordination.pcoa(dm_u, method='fsvd', number_of_dimensions=20)
t2=time.time()
print("=== %s PCOA=20 time:  %.2f"%(sys.argv[1], t2-t1))
print(pc)


