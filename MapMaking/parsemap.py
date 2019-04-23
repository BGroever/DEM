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
    print(county)
    reffile += '{}\t{}\t{}\n'.format(re.findall(r'(^.*\w(?=__\w\w)|^.*\w(?=_\w\w))', county)[0].replace('"',"").replace("_"," ").strip(), re.findall(r'[A-Z]{2}"$',county)[0].replace('"',""), tuple(int(newcolor[i:i+2], 16) for i in (0, 2, 4)))

script = script[:-1]
script += '},"title":"","hidden":[],"background":"#ffffff","borders":""}'

with open("FinalScript.txt", "w") as temp_file:
    temp_file.write(script)

with open("ReferenceFileWithStates.txt",'w') as temp_file:
    temp_file.write(reffile)
