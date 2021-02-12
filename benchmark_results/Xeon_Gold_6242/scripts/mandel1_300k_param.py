import h5py
import skbio

import time

import sys

slice=int(sys.argv[1])
print("Proessing %i * %i matrix"%(slice,slice))

t1=time.time()
with h5py.File("v300k_uw32.h5","r") as f_u:
 dm_u=skbio.stats.distance.DistanceMatrix(f_u['matrix'][:slice,:slice],f_u['order'][:slice])

with h5py.File("v300k_wn32.h5","r") as f_u:
 dm_w=skbio.stats.distance.DistanceMatrix(f_u['matrix'][:slice,:slice],f_u['order'][:slice])


t2=time.time()
print("H5 %.2f"%(t2-t1))


# example computing a mantel test
t1=time.time()
r, p, n = skbio.stats.distance.mantel(dm_u, dm_w)
t2=time.time()
print("MT %.2f"%(t2-t1))

print(r, p, n)
