import re
import string

with open('mapchartALL_parsed.txt', 'r') as temp_file:
    data = temp_file.readlines()

allcty = data[0].split(',')

script = '{"groups":{'
color = 0
for count, county in enumerate(allcty):
    color += 2
    script += '"#{}":{{"div":"#box{:d}","label":"","paths":[{}]}},'.format(hex(color).split('x')[-1], count+1, county)

script = script[:-1]
script += '}},"title":"","hidden":[],"background":"#ffffff","borders":""}}'

with open("FinalScript.txt", "w") as temp_file:
    temp_file.write(script)
