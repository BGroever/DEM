import re

with open("colchart_counties.txt","r") as temp_file:
    data = temp_file.readlines()

list_fips = []
for line in data:
    a1,a2,a3,fips = line.split()
    list_fips.append(int(fips))

with open("den_per_county.txt","r") as temp_file:
    data2 = temp_file.readlines()

list_pop = []
for line in data2:
    pop, fips = line.split()
    list_pop.append(int(fips))

print("Den fips not in colfips:")
for pop in list_pop:
    if pop not in list_fips:
        print("Line {}: fips = {}".format(list_pop.index(pop),pop))

print("Fips not in Den:")
for fips in list_fips:
    if fips not in list_pop:
        print("Line {}: fips = {}".format(list_fips.index(fips),fips))
