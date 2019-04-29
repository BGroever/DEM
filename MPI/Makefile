# C compiler
cxx=gcc
mpi=mpicc

# Compilation flags
cflags=-pedantic -Wall -O3
openmp=-pedantic -Wall -O3 -fopenmp

# Flags for PNG library
png_lflags=-lm -lpng

execs=exec.x exec.mpi exec.openmp

all: $(execs)

clean:
	rm -f $(execs)

exec.x: dem_serial.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)

exec.mpi: dem_mpi.c
	$(mpi) $(cflags) -o $@ $^ $(png_lflags)

exec.openmp: dem_openmp.c
	$(mpi) $(openmp) -o $@ $^ $(png_lflags)
