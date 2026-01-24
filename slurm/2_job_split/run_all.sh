jobidA=$(sbatch --parsable ./map_optimize.sh)
echo $jobidA
jobidB=$(sbatch --parsable --dependency=afterok:$jobidA ./execute.sh)
echo $jobidB
jobidC=$(sbatch --parsable --dependency=afterok:$jobidB ./result.sh)
echo $jobidC
