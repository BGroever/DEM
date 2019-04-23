import re

with open("CtyFIPS.txt","r") as temp_file:
    dataF = temp_file.readlines()

with open("ReferenceFileWithStates.txt","r") as temp_file:
    dataR = temp_file.readlines()

with open("StateFIPS.txt", "r") as temp_file:
    dataS = temp_file.readlines()

state_fips = {}

for line in dataS:
    state, fips = line.split('\t')
    state_fips[state]=int(fips)

FinalRef = ''
counter1 = 0
counter2 = 0
for count, line in enumerate(dataF):
    #print("Count: ", count, " line: ", line.replace("\n",""))
    cty, fips = line.split('\t')
    cty = cty.strip()
    if cty == 'Saint Clair':
        cty = 'St Clair'
    elif cty == 'Hoonah-Angoon':
        cty = 'Hoonah'
    elif cty == 'Juneau City and':
        cty = 'Juneau'
    elif cty == 'Matanuska-Susitna':
        cty = 'MatanuskaSusitna'
    elif cty == 'Prince of Wales-Hyder':
        cty = 'Prince of Wales Hyder'
    elif cty == 'Sitka City and':
        cty = 'Sitka'
    elif cty == 'Southeast Fairbanks':
        cty = 'Fairbanks'
    elif cty == 'Valdez-Cordova':
        cty = 'ValdezCordova'
    elif cty == 'Wrangell City and':
        cty = 'Wrangell'
    elif cty == 'Yakutat City and':
        cty = 'Yakutat'
    elif cty == 'Yukon-Koyukuk':
        cty = 'YukonKoyukuk'
    elif cty == 'Saint Francis':
        cty = 'St Francis'
    elif cty == 'Rio Grande':
        cty = 'Rio Grande'
    elif cty == 'Miami-Dade':
        cty = 'Miami'
    elif cty == 'Saint Johns':
        cty = 'St Johns'
    elif cty == 'Saint Lucie':
        cty = 'St Lucie'
    elif cty == 'Saint Joseph':
        cty = 'St Joseph'
    elif cty == 'Saint Mary s':
        cty = 'St Mary s'
    elif cty.split()[0]=='Saint':
        cty = 'St'+' '+cty.split()[1]
    fips = fips.strip()
    counter1 += 1
    found = 0
    for lineR in dataR:
        ctyR, stateR, RGBR = lineR.split('\t')
        if cty in lineR and int(float(fips)/1000)==state_fips[stateR]:
            FinalRef += line.replace("\n","") + '\t' + re.findall(r'\(\d+,\ \d+,\ \d+\)', lineR)[0].replace(" ","") + '\n'
            dataR.remove(lineR)
            counter2 += 1
            found = 1
            break
    if not found:
        if cty == 'Rio Grande':
            FinalRef += line.replace("\n","") + '\t' + '(255,247,214)\n'
            counter2+=1
        elif cty == 'Clayton':
            FinalRef += line.replace("\n","") + '\t' + '(255,233,98)\n'
            counter2 += 1
        elif cty == 'Greenup':
            FinalRef += line.replace("\n","") + '\t' + '(255,218,108)\n'
            counter2 += 1
        elif cty == 'LaSalle':
            FinalRef += line.replace("\n","") + '\t' + '(255,214,42)\n'
            counter2 += 1
        elif cty == 'Lake of the Woods':
            FinalRef += line.replace("\n","") + '\t' + '(255,210,106)\n'
            counter2 += 1
        elif cty == 'Red Lake':
            FinalRef += line.replace("\n","") + '\t' + '(255,210,76)\n'
            counter2 += 1
        elif cty == 'Jefferson Davis':
            FinalRef += line.replace("\n","") + '\t' + '(255,133,248)\n'
            counter2 += 1
        elif cty == 'Scotts Bluff':
            FinalRef += line.replace("\n","") + '\t' + '(255,191,0)\n'
            counter2 += 1
        elif cty == 'Allegany':
            FinalRef += line.replace("\n","") + '\t' + '(255,212,24)\n'
            counter2 += 1
        elif cty == 'Saint Lawrence':
            FinalRef += line.replace("\n","") + '\t' + '(255,133,248)\n'
            counter2 += 1
        elif cty == 'Adams':
            FinalRef += line.replace("\n","") + '\t' + '(255,232,224)\n'
            counter2 += 1
        elif cty == 'Williamson':
            FinalRef += line.replace("\n","") + '\t' + '(255,228,78)\n'
            counter2 += 1
        elif cty == 'Chesterfield':
            FinalRef += line.replace("\n","") + '\t' + '(255,172,254)\n'
            counter2 += 1
        elif cty == 'Jackson':
            FinalRef += line.replace("\n","") + '\t' + '(255,157,234)\n'
            counter2 += 1
        elif cty == 'Robertson':
            FinalRef += line.replace("\n","") + '\t' + '(255,157,234)\n'
            counter2 += 1
        elif cty == 'Charlottesville':
            FinalRef += line.replace("\n","") + '\t' + '(255,152,244)\n'
            counter2 += 1
        elif cty == 'Manassas Park':
            FinalRef += line.replace("\n","") + '\t' + '(255,151,60)\n'
            counter2 += 1
        else:
            print("Not Found:", line.replace("\n",""))


with open("MapReference.txt", "w") as temp_file:
    temp_file.write(FinalRef)

print("Counter1 = {} and Counter2 = {}".format(counter1, counter2))

