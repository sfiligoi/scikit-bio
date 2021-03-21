#!/bin/bash
hostname
lscpu
date

export OMP_NUM_THREADS=8

source ~/setup_conda.source
conda activate skbio-local

for i in 20 25; do 
taskset -c 0-7 time python ../../scripts/mantel.py "${i}000 fp64" ../../inputs/unifrac_${i}000_pcoa_10.fp64.h5 ../../inputs/unifrac_${i}000_nf_pcoa_0.fp64.h5
done
