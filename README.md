# Density equalizing map

Density-equalizing maps, also known as cartograms, are an effective communication tool to represent economic, political or social differences across a geographical region. While most algorithms focus on speed rather than topological accuracy, the diffusion-based method is one of the few ways that guarantees topology preservation and yields a topological exact representation. Nevertheless, to avoid the high computational cost, inexact methods are often used instead, which can result in topological distortions as they don't algorithmically guarantee preservation. Particularly for high-resolution images, the computational cost of the diffusion approach outweighs the benefits in accuracy. In our CS205 project, we address this problem with a software package which is easily deployed from Github on any multicore/multinode cluster and or laptop. From an input image file, the user can obtain a density equalized map with significant speedup. In our tutorial, we illustrate this for the 2016 US election map. On our GitHub website, we show the package scales linearly up to 2 nodes with 8 threads each, which is the size limitation of our cluster.

# Usage

The libpng package for I/O can be installed on Linux as:

```Bash
sudo apt-get install libpng-dev
```

and installed on Mac OSX as:

```Bash
brew install libpng
```
## MPI and OpenMP
The code can be compiled using the command:
```Bash
make
```
This will generate the serial, the MPI and the hybrid executables. The hybrid executable run for the US county image as:
```Bash
threads=4
task=2
export OMP_NUM_THREADS=$threads;
mpirun -np $tasks -genv OMP_NUM_THREADS $threads ./exec.openmp "uscounties10.png" "col_counties.txt" "counties.txt" "output.png"
```
The files `openmp.sh` and `mpi.sh` generate the MPI/OpenMP speedup diagram on Odyssey with the command:
```Bash
sbatch openmp.sh
```
The standard output will be `mpi.out` and `openmp.out` respectively. If you want to run a different data set beside US counties you need change the SIZE on top of the main file `dem_openmp.c`.

## CUDA


# Acknowledgement

The code for the two functions `write_png_file()` and `read_png_file()` were scavenged from another [Github site](https://gist.github.com/niw/5963798).
