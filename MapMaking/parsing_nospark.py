import re

with open("FIPS_COUNTY_NOSTATE.txt","r") as temp_file:
    data = temp_file.readlines()


final_list = ''

for x in data:
    if x.startswith('District'):
        print('Here')
        print(x)
        final_list += 'Washington__DC\n'
    elif 'County' in x:
        new_string = re.findall(r"^[\w\s'-]+(?=County)", x)[0].replace(" "," ").replace("'"," ")+'\t'+re.findall(r"[\d]+$", x)[0] #"__"+re.findall(r"\w[\w\s]+(?=\s\d+)", x)[0].replace(" ","_")
        final_list += new_string + '\n'
    elif 'Borough' in x:
        new_string = re.findall(r"^[\w\s'-]+(?=Borough)", x)[0].replace(" "," ").replace(" "," ")+'\t'+re.findall(r"[\d]+$", x)[0] #+"__"+re.findall(r"\w[\w\s]+(?=\s\d+)", x)[0].replace(" ","_")
        final_list += new_string + '\n'
    elif 'Census Area' in x:
        new_string = re.findall(r"^[\w\s'-]+(?=Census Area)", x)[0].replace(" "," ").replace(" "," ")+'\t'+re.findall(r"[\d]+$", x)[0] #+"__"+re.findall(r"\w[\w\s]+(?=\s\d+)", x)[0].replace(" ","_")
        final_list += new_string + '\n'
    elif 'Municipality' in x:
        new_string = re.findall(r"^[\w\s'-]+(?=Municipality)", x)[0].replace(" "," ").replace(" "," ")+'\t'+re.findall(r"[\d]+$", x)[0] #+"__"+re.findall(r"\w[\w\s]+(?=\s\d+)", x)[0].replace(" ","_")
        final_list += new_string + '\n'
    elif 'City' in x:
        new_string = re.findall(r"^[\w\s'-]+(?=City)", x)[0].replace(" "," ").replace(" "," ")+'\t'+re.findall(r"[\d]+$", x)[0] #+"__"+re.findall(r"\w[\w\s]+(?=\s\d+)", x)[0].replace(" ","_")
        final_list += new_string + '\n'
    elif 'Parish' in x:
        new_string = re.findall(r"^[\w\s'-]+(?=Parish)", x)[0].replace(" "," ")+'\t'+re.findall(r"[\d]+$", x)[0] #+"__"+re.findall(r"\w[\w\s]+(?=\s\d+)", x)[0].replace(" ","_")
        final_list += new_string + '\n'
    else:
        print(x)


with open("CtyFIPS.txt","w") as temp_file:
    temp_file.write(final_list)
