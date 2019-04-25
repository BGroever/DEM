# C compiler
cxx=gcc-8

# Compilation flags
cflags=-fopenmp -pedantic -Wall -O3 -I/usr/local/include -L/usr/local/lib #-DUSE_CLOCK

# Flags for PNG library
png_lflags=-lm -lpng

execs=exec.x

all: $(execs)

clean:
	rm -f $(execs)

exec.x: dem.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)
