# C compiler
cxx=gcc-8

# Compilation flags
cflags=-fopenmp -pedantic -Wall -O3 -I/usr/local/include -L/usr/local/lib -L$HOME/mpich/mpich2/lib #-DUSE_CLOCK

# Flags for PNG library
png_lflags=-lm -lpng -lz -w -lmpi

execs=exe_mpi.x exe_ser.x exe_openmp.x

all: $(execs)

clean:
	rm -f $(execs)

exe_mpi.x: dem_mpi.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)

exe_ser.x: dem_serial.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)

exe_openmp.x: dem_openmp.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)
