import sys
import h5py
import skbio
import numpy as np

import time

if sys.argv[1].find('fp32')==-1:
  print("Using fp64 version")
  dt=np.float64
else:
  print("Using fp32 version")
  dt=np.float32


t1=time.time()
with h5py.File(sys.argv[2],"r") as f_u:
  mt = np.asarray(f_u['matrix'][:,:],dtype=dt)
  ord=f_u['order'][0:]

dm_u=skbio.stats.distance.DistanceMatrix(mt,ord)

t2=time.time()
print("=== %s FileLoad time: %.2f"%(sys.argv[1], t2-t1))


