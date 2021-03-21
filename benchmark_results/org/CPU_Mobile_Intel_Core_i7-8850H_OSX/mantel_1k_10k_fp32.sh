#!/bin/bash
hostname
sysctl -n machdep.cpu -N |head -20
date

export OMP_NUM_THREADS=6

source ../../setup_conda.source
conda activate unifrac-cpu

for i in 1 2 5 10; do 
/usr/bin/time python ../../scripts/mantel.py "${i}000 fp32" ../../inputs/unifrac_${i}000_pcoa_10.h5 ../../inputs/unifrac_${i}000_nf_pcoa_0.h5
done
