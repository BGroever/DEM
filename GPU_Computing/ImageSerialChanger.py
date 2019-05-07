from skimage import io
import numpy as np
import os

idir = 'Snapshots10'
fdir = 'Snapshots10uselections'

dict_fips = {}
dict_no = {}
with open("colchart_counties.txt","r") as temp_file:
    data = temp_file.readlines()
for line in data:
    r,g,b = [int(itm) for itm in line.split()[:-1]]
    co = r+256*g+65536*b
    dict_fips[co]=int(line.split()[-1])

with open("Dem2016.txt","r") as temp_file:
    data = temp_file.readlines()
for line in data:
    dict_no[int(line.split()[-1])]=[int(itm) for itm in line.split()[:-1]]

for filename in os.listdir(idir):
    if filename.startswith("time"):
        print(filename)
        o=io.imread("{}/{}".format(idir,filename))
        (m,n,z)=o.shape



        no=np.zeros((m,n,4))
        no = np.empty((m,n,4), dtype=np.uint8)
        badfps = []
        for i in range(m):
            for j in range(n):
                r,g,b = o[i,j,:3]
                co=o[i,j,0]+256*o[i,j,1]+65536*o[i,j,2]
                if co == 16777215:
                    no[i,j,0] = 255
                    no[i,j,1] = 255
                    no[i,j,2] = 255
                    no[i,j,3] = 255
                elif dict_fips[co] in dict_no.keys():
                    no[i,j,:-1] = dict_no[dict_fips[co]]
                    no[i,j,3] = 255
                elif dict_fips[co]==15005:
                    no[i,j,:-1] = dict_no[15009]
                    no[i,j,3] = 255
                elif dict_fips[co]==2158:
                    no[i,j,0] = 255
                    no[i,j,1] = 255
                    no[i,j,2] = 255
                    no[i,j,3] = 255

                else:
                    if dict_fips[co] not in badfps:
                        badfps.append(dict_fips[co])
        if len(badfps)!=0:
            print(badfps)
        io.imsave("{}/{}".format(fdir,filename),no)

