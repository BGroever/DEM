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
plt.plot(p_list, p_list, label = 'Linear Speedup', color = 'k', linewidth=2)
plt.plot(p_list, list(map(f,p_list)), label = 'Amdahl', color = '#cc0000',linewidth=2)
N=5000
plt.plot(p_list, list(map(Sth,p_list)), alpha=0.5,label = 'Spx : 5000x5000 px', color = '#14a323') #color = '#1fc200') #color = '#004c99')
N=3000
plt.plot(p_list, list(map(Sth,p_list)), alpha=0.5,label = 'Spx : 3000x3000 px', color = '#00bf13') #color = '#1fc200') #color = '#004c99')
N=1500
plt.plot(p_list, list(map(Sth,p_list)), alpha=0.5,label = 'Spx : 1500x1500 px', color = '#00c654') #color = '#1fc200') #color = '#004c99')
N=1000
plt.plot(p_list, list(map(Sth,p_list)), alpha=0.5,label = 'Spx : 1000x1000 px', color = '#00ce9a') #color = '#00d280') #color = '#0080ff')
N=500
plt.plot(p_list, list(map(Sth,p_list)), alpha=0.5,label = 'Spx : 500x500 px', color = '#00c5d5') #color = '#00d9d9') #color = '#66b2ff')
N=300
plt.plot(p_list, list(map(Sth,p_list)), alpha=0.5,label = 'Spx : 300x300 px', color = '#00a5d9') #color='#005fe5') #, color='#99ccff')
N=200
plt.plot(p_list, list(map(Sth,p_list)), alpha=0.5,label = 'Spx : 200x200 px', color = '#0084dd') #color='#005fe5') #, color='#99ccff')
N=100
plt.plot(p_list, list(map(Sth,p_list)), alpha=0.5,label = 'Spx : 100x100 px', color='#003ee5') # color='#005fe5') #, color='#99ccff')

#plt.plot(p_list, list(map(S,p_list)), label = 'Hardware')
plt.legend(loc = 'upper left')
plt.grid(which = 'both')
plt.xlim([0,1024])
plt.xlabel('Number of computing cores', fontweight = 'bold', fontsize = 12)
plt.ylabel('Speedup', fontweight = 'bold', fontsize = 12)
plt.title('Speedup as a function of number of cores.', fontweight = 'bold', fontsize = 14)
plt.ylim([0, 1050])
plt.savefig('ThSpeedupLow.png')
plt.show()
