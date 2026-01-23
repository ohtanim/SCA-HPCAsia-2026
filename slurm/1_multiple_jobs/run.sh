jobidA=$(sbatch run_sampler.sh | awk '{print $4}')
sbatch --dependency=afterok:$jobidA /shared/job_scripts/mpi/get_counts/get_counts_job.sh
