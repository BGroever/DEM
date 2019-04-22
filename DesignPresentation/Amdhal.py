import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

c =0.9996
f = lambda p: 1/((1-c)+(c/p))

p_list = np.arange(1,1024)


N=100
tsm = 18.4e-9
tnode = 65e-9
tproc = 0.08e-9
toff = 27e-3
T = N*N/6
dt = 0.24

def Sth(p):
    return (0+(1)*(N*N*tsm))/(0+(1)*((N*N/p)*tsm + ((N/np.sqrt(p))-(N/np.sqrt(np.ceil(1+(p/4)))))*tproc + (N/np.sqrt(np.ceil(1+(p/4))))*tnode))

def S(p):
    return (toff+(T/dt)*(N*N*tsm))/(toff+(T/dt)*((N*N/p)*tsm + ((N/np.sqrt(p))-(N/np.sqrt(np.ceil(1+(p/4)))))*tproc + (N/np.sqrt(np.ceil(1+(p/4))))*tnode))




plt.figure()
plt.plot(p_list, p_list, label = 'Linear Speedup', color = 'k')
plt.plot(p_list, list(map(f,p_list)), label = 'Amdhal', color = '#cc0000')
N=100
plt.plot(p_list, list(map(Sth,p_list)), label = 'Hardware : 100x100 px', color='#005fe5') #, color='#99ccff')
N=500
plt.plot(p_list, list(map(Sth,p_list)), label = 'Hardware : 500x500 px', color = '#00d9d9') #color = '#66b2ff')
N=1000
plt.plot(p_list, list(map(Sth,p_list)), label = 'Hardware : 1000x1000 px', color = '#00d280') #color = '#0080ff')
N=1500
plt.plot(p_list, list(map(Sth,p_list)), label = 'Hardware : 1500x1500 px', color = '#1fc200') #color = '#004c99')

#plt.plot(p_list, list(map(S,p_list)), label = 'Hardware')
plt.legend(loc = 'upper left')
plt.grid(which = 'both')
plt.xlim([0,1024])
plt.xlabel('Number of computing cores', fontweight = 'bold', fontsize = 12)
plt.ylabel('Speedup', fontweight = 'bold', fontsize = 12)
plt.title('Speedup as a function of number of cores.', fontweight = 'bold', fontsize = 14)
plt.ylim([0, 1050])
plt.savefig('ThSpeedup.png')
plt.show()
