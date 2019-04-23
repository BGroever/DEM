from skimage import io
import numpy as np

o=io.imread('US_Counties.png')
(m,n,z) = o.shape
list_colors = []
for i in range(m):
    for j in range(n):
        colr = '#{}{}{}'.format(hex(o[i,j,0])[2:],hex(o[i,j,1])[2:],hex(o[i,j,2])[2:])
        # colr = o[i,j,:]
        if colr not in list_colors:
            print(colr)
            list_colors.append(colr)
        #print("({},{},{})".format(o[i,j,0],o[i,j,1],o[i,j,2]))

print("Size list : {}".format(len(list_colors)))
