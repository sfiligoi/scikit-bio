#!/bin/bash
hostname
lscpu
date

export OMP_NUM_THREADS=4

source ~/unifrac/conda_setup.sh
conda activate skbio-local

for i in 20 25 30; do 
taskset -c 0-4 time python ../../scripts/mantel_spearman.py "${i}000 fp32" ../../inputs/unifrac_${i}000_pcoa_10.h5 ../../inputs/unifrac_${i}000_nf_pcoa_0.h5
done
