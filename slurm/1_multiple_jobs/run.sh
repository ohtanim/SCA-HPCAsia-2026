jobidA=$(sbatch run_sampler.sh | awk '{print $4}')
sbatch --dependency=afterok:$jobidA get_counts_job.sh
