#!/bin/bash
#SBATCH -J county
#SBATCH -o county.out
#SBATCH -e county.err
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -c 8
#SBATCH -t 1-00:00
#SBATCH --mem-per-cpu=4000
#SBATCH --account=weitz_lab


#Use this version of gcc on odyssy it already includes libpng
module purge
module load gcc/7.1.0-fasrc01 openmpi/3.1.1-fasrc01
rm -rf exec.*
make

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
srun -n $SLURM_NTASKS --cpus-per-task=$SLURM_CPUS_PER_TASK --mpi=pmi2 ./exec.openmp "uscounties.png" "colchart_counties.txt" "den_per_county.txt"


