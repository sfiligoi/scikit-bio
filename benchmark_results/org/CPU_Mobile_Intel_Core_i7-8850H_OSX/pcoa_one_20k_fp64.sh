#!/bin/bash
hostname
sysctl -n machdep.cpu -N |head -20
date

export OMP_NUM_THREADS=6

source ../../setup_conda.source
conda activate unifrac-cpu

for i in 20 ; do 
/usr/bin/time -l python ../../scripts/pcoa_load_only.py "${i}000 fp64" ../../inputs/unifrac_${i}000_pcoa_10.fp64.h5
/usr/bin/time -l python ../../scripts/pcoa_inline.py "${i}000 fp64" ../../inputs/unifrac_${i}000_pcoa_10.fp64.h5
/usr/bin/time -l python ../../scripts/pcoa_one.py "${i}000 fp64" ../../inputs/unifrac_${i}000_pcoa_10.fp64.h5
done
