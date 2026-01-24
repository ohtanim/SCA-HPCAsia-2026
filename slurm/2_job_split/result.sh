#!/bin/bash

#SBATCH --job-name=result
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
echo "Current working directory is `pwd`"

# Your script goes here
source /shared/pyenv/bin/activate
srun python ./result.py sampler_output_ibm_fez.json
