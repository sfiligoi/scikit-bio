#!/bin/bash
hostname
lscpu
date

export OMP_NUM_THREADS=8


source ~/setup_conda.source
conda activate unifrac-202

for i in 1 2 5 10 20 25; do 
taskset -c 0-7 time python ../../scripts/pcoa.py "${i}000 fp32" ../../inputs/unifrac_${i}000_pcoa_10.h5 
done
