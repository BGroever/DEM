# C compiler
cxx=gcc

# Compilation flags
cflags=-pedantic -Wall -O3 -DUSE_CLOCK

# Flags for PNG library
png_lflags=-lm -lpng

execs=exec.x

all: $(execs)

clean:
	rm -f $(execs)

exec.x: diff_map2.c
	$(cxx) $(cflags) -o $@ $^ $(png_lflags)
