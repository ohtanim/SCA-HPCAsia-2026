#!/bin/bash

#SBATCH --qpu=ibm_fez
#SBATCH --job-name=job_split_hetjob
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition normal

#SBATCH hetjob

#SBATCH --gres=qpu:1
#SBATCH --qpu=ibm_fez
#SBATCH --partition quantum

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
echo "Current working directory is `pwd`"

# Your script goes here
source /shared/pyenv/bin/activate
srun --het-group=0 python map_optimize.py
srun --het-group=1 task_runner ibm_fez sampler_input_ibm_fez.json sampler_output_ibm_fez.json
srun --het-group=0 python result.py sampler_output_ibm_fez.json
