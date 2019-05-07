with open("year2015raw.txt", "r") as temp_file:
    data = temp_file.readlines()

optxt = ''
gdplist = []
dict_fips = {}
for line in data:
    gdp, fips = line.split()
    if int(fips) not in dict_fips.keys():
        dict_fips[int(fips)]=int(gdp)
        gdplist.append(int(gdp))
maxgdp = max(gdplist)
for fips in dict_fips.keys():
    optxt += '{:.3f} {}\n'.format(1000*float(dict_fips[fips]/maxgdp), fips)
#        optxt += '{} {}\n'.format(int(gdp),int(fips))

with open("year2015.txt","w") as temp_file:
    temp_file.write(optxt)

