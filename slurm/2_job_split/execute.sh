#!/bin/bash

#SBATCH --job-name=execute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=qpu:1
#SBATCH --qpu=ibm_fez
#SBATCH -p quantum

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
echo "Current working directory is `pwd`"

# Your script goes here
source /shared/pyenv/bin/activate
srun task_runner ibm_fez sampler_input_ibm_fez.json sampler_output_ibm_fez.json
