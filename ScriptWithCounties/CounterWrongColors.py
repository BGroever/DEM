import re

with open("opt.dat","r") as temp_file:
    data = temp_file.readlines()

list_clr = []
for line in data:
    if line.startswith("Mayday Mayday"):
        clr = int(re.findall('\d\d+$', line)[0])
        if clr not in list_clr:
            list_clr.append(clr)

print("Len = ",len(list_clr))
print(list_clr)
for clr in list_clr:
    B = int(clr/65536)
    new_clr = clr - B*65536
    G = int(new_clr/256)
    R = new_clr - G*256
    print("Color = {:d} = ({},{},{})".format(clr, R,G,B))

