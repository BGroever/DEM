with open("err.dat","r") as temp_file:
    data = temp_file.readlines()

errs = []
for line in data:
    if line.startswith("Mayday"):

