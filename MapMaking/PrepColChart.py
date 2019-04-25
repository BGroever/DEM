import re

with open("CountyColorsForMillie.txt","r") as temp_file:
    data = temp_file.readlines()


colchart = ''

for line in data:
    cty, fips, rgb = line.split('\t')
    R,G,B = rgb.replace('\n','').replace("(","").replace(")","").split(',')
    colchart += '{} {} {} {}\n'.format(R,G,B,fips)

with open('colchart_counties.txt','w') as temp_file:
    temp_file.write(colchart)
