#!/bin/bash
#SBATCH -J openmp
#SBATCH -o openmp.out
#SBATCH -e openmp.err
#SBATCH -p shared
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 7
#SBATCH -t 0-60:00
#SBATCH --mem-per-cpu=4000
#SBATCH --account=ingber_lab


#This version of gcc on odyssy it already includes libpng
module purge
module load gcc/7.1.0-fasrc01 openmpi/3.1.1-fasrc01
rm -rf exec.*
make

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
srun -n $SLURM_NTASKS --cpus-per-task=$SLURM_CPUS_PER_TASK --mpi=pmi2 ./exec.openmp "uscounties10.png" "col_counties.txt" "counties.txt" "output.png"
