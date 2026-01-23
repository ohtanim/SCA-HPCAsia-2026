#!/bin/bash

#SBATCH --job-name=sampler
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=qpu:1
#SBATCH --qpu=ibm_kingston

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
echo "Current working directory is `pwd`"

# Your script goes here
source /shared/tutorial/pyenv/bin/activate
srun python /shared/tutorial/getting_started/sampler_qrmi.py
