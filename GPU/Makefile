# C compiler
cxx=gcc-8
nxx=nvcc

# Compilation flags
cflags=-fopenmp -pedantic -Wall -O3 -I/usr/local/include -L/usr/local/lib -L/home/ubuntu/mpich/mpich2/lib 
gflags=-ccbin=mpic++ -arch=sm_50

# Flags for PNG library
png_lflags=-lm -lpng -lz -w -lmpi
gpng_lflags=-lpng -Xptxas -O3

objs=dem_mpi_gpu.o
src=$(patsubst %.o,%.c,$(objs))
execs=exe_gpu.x

executables: $(execs)

%.o: %.c
	$(cxx) $(cflags) -o $@ -c $<

dem_mpi_gpu.o: dem_mpi_gpu.c
	$(cxx) -c $< -o $@ $(cflags)

clean:
	rm -f $(execs) $(objs)

exe_gpu.x: dem_cuda.cu dem_mpi_gpu.o 
	$(nxx) $(gflags) -o $@ $^ $(gpng_lflags)

