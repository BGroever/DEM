with open("den_per_county.txt", "r") as temp_file:
    data_den = temp_file.readlines()

with open("colchart_counties.txt", "r") as temp_file:
    data_col = temp_file.readlines()

county_col = {}

for line in data_col:
    county_col[int(line.split()[-1])] = [int(itm) for itm in line.split()[:3]]

county_den = {}
for line in data_den:
    county_den[int(line.split()[-1])] = float(line.split()[0])

print("Size of county_den_keys = {} and Size of county_col_keys={}".format(len(county_den.keys()), len(county_col.keys())))
for key_den in county_den.keys():
    if key_den not in county_col:
        print("key_den {:d} is not in colchart_counties...".format(key_den))

for key_col in county_col.keys():
    if key_col not in county_den:
        print("key_col {:d} is not in den_per_counties...".format(key_col))
        
