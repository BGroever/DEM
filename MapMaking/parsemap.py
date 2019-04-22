import re
import string

with open('mapchartALL_parsed.txt', 'r') as temp_file:
    data = temp_file.readlines()

allcty = data[0].split(',')

script = '{"groups":{'
color = 16777216

reffile = ''

for count, county in enumerate(allcty):
    color -= 10
    newcolor = hex(color)[2:].zfill(6)
    script += '"#{}":{{"div":"#box{:d}","label":"","paths":[{}]}},'.format(newcolor, count+1, county)
    reffile += '{}\t{}\n'.format(county, newcolor)

script = script[:-1]
script += '}},"title":"","hidden":[],"background":"#ffffff","borders":""}}'

with open("FinalScript.txt", "w") as temp_file:
    temp_file.write(script)

with open("ReferenceFile.txt",'w') as temp_file:
    temp_file.write(reffile)
