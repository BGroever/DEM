import re

with open("raw_den.txt","r") as temp_file:
    data = temp_file.readlines()

final_scr = ''
for line in data:
    den, ids = line.split('\t')
    st, fips = re.findall('(\d{7})US(\d+)',ids)[0]
    if (int(st) == 500000) and (int(fips.replace("\n","")) <72000):
        final_scr += '{}\t{}\n'.format(den,int(fips.replace("\n","")))

with open("den_per_county.txt","w") as temp_file:
    temp_file.write(final_scr)

