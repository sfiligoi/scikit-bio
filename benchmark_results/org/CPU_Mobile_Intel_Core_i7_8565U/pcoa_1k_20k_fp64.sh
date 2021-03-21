#!/bin/bash
hostname
lscpu
date

export OMP_NUM_THREADS=4

source ~/unifrac/conda_setup.sh
conda activate unifrac-gpu

for i in 1 2 5 10 20; do 
taskset -c 0-3 time python ../../scripts/pcoa.py "${i}000 fp64" ../../inputs/unifrac_${i}000_pcoa_10.fp64.h5 
done
