import sys
import h5py
import skbio

import time

t1=time.time()
with h5py.File(sys.argv[2],"r") as f_u:
 dm_u=skbio.stats.distance.DistanceMatrix(f_u['matrix'][:,:],f_u['order'][:])

with h5py.File(sys.argv[3],"r") as f_u:
 dm_w=skbio.stats.distance.DistanceMatrix(f_u['matrix'][:,:],f_u['order'][:])


t2=time.time()
print("=== %s FileLoad time: %.2f"%(sys.argv[1], t2-t1))


# example computing a mantel test
t1=time.time()
r, p, n = skbio.stats.distance.mantel(dm_u, dm_w)
t2=time.time()
print("=== %s Mantel time: %.2f"%(sys.argv[1], t2-t1))

print(r, p, n)
