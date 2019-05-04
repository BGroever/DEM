# C compiler
cxx=gcc
mpi=mpicc

# Compilation flags
cflags=-O3 #-pedantic -Wall
openmp=-O3 -fopenmp -pedantic -Wall #-fopt-info-vec-missed -g

# Flags for PNG library
png_lflags=-lm -lpng -I/usr/local/include -L/usr/local/lib

execs=exec.x exec.mpi exec.openmp

all: $(execs)

clean:
	rm -f $(execs)

exec.x: dem_serial.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)

#exec.mpi: dem_mpi.c
#	$(mpi) $(cflags) -o $@ $^ $(png_lflags)

exec.openmp: dem_openmp.c
	$(mpi) $(openmp) -o $@ $^ $(png_lflags)
