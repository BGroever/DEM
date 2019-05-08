import numpy as np
import re

dict_col = {}
with open("colmap.txt", "r") as temp_file:
    data = temp_file.readlines()

for count, line in enumerate(data):
    h = line.split()[0].lstrip('#')
    r,g,b = [int(h[i:i+2],16) for i in (0,2,4)]
    dict_col[count] = '{} {} {}'.format(r,g,b)


with open("Election2016.txt","r") as temp_file:
    data = temp_file.readlines()

optxt = ''
for line in data[1:]:
    fips = int(line.split(',')[-1])
    dem = float(line.split(',')[1])
    rep = float(line.split(',')[2])
    ttl = float(line.split(',')[3])
    pct = np.round(100*(dem/ttl))
    rgb = dict_col[pct]
#    if pct <10:
#        rgb = '211 26 23'
#    elif pct < 20:
#        rgb = '196 32 39'
#    elif pct < 30:
#        rgb = '181 39 56'
#    elif pct < 40:
#        rgb = '166 45 72'
#    elif pct < 50:
#        rgb = '136 58 105'
#    elif pct < 60:
#        rgb = '105 70 137'
#    elif pct < 70:
#        rgb = '90 77 154'
#    elif pct < 80:
#        rgb = '60 89 186'
#    elif pct < 90:
#        rgb = '45 96 203'
#    else:
#        rgb = '30 102 219'

    optxt += '{} {}\n'.format(rgb, fips)

with open("Dem2016.txt", "w") as temp_file:
    temp_file.write(optxt)

