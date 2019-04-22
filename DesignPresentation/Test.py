import numpy as np

N=1430
tsm = 18.4e-9
tnode = 65e-9
tproc = 50e-9
toff = 27e-3
T = N*N/6
dt = 0.24

def myf(p):
    return ((N/np.sqrt(p))-(N/np.sqrt(np.ceil(1+(p/4)))))*tproc + (N/np.sqrt(np.ceil(1+(p/4))))*tnode

p = np.arange(1, 64)

[print(myf(itm)) for itm in p]
