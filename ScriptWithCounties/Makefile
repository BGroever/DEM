# C compiler
cxx=gcc-8

# Compilation flags
cflags=-fopenmp -pedantic -Wall -O3 -I/usr/local/include -L/usr/local/lib #-DUSE_CLOCK

# Flags for PNG library
png_lflags=-lm -lpng

execs=exe_par.x exe_ser.x exe_parv2.x

all: $(execs)

clean:
	rm -f $(execs)

exe_par.x: dem.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)

exe_ser.x: dem_serial.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)

exe_parv2.x: demv2.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)
