import numpy as np
import scipy
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.font_manager
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

with open("speedup.dat","r") as temp_file:
    data = temp_file.readlines()

threads = []
xtimes = []
xsrd=[]
xmin = []
xmax = []

for line in data:
    th, th2 = [int(itm) for itm in line.split()[:2]]
    t1, t2, t3, t4, t5 = [float(itm) for itm in line.split()[2:]]
    threads.append(th)
    meant = np.mean(np.array([t1,t2,t3,t4,t5]))
    stdt = np.std(np.array([t1,t2,t3,t4,t5]))
    mint = np.min(np.array([t1,t2,t3,t4,t5]))
    maxt = np.max(np.array([t1,t2,t3,t4,t5]))
    xtimes.append(meant)
    xsrd.append(stdt)
    xmin.append(mint)
    xmax.append(maxt)

spd = np.array([xtimes[-1]/itm for itm in xtimes])
maxspd = np.array([xmax[-1]/itm for itm in xmin])
minspd = np.array([xmin[-1]/itm for itm in xmax])
ye = maxspd-spd
yem = spd-minspd
print("Spd:", spd)
print("maxspd",maxspd)
print("minspd",minspd)
fig, ax = plt.subplots(figsize = (8,6))
#ax.plot(threads[:-1],spd,'o')
ax.errorbar(threads,spd, yerr= [yem, ye],fmt='--o', color = '#c64d1d')
plt.grid(which='both')
plt.xlim([0,11])
plt.ylim([1,1.7])
plt.xlabel(r"$log_2\left(\mathrm{threads}\right)$", fontsize = 14)
plt.ylabel(r"Speedup", fontsize = 14)
plt.title("Speedup as a function of the number of threads, for a GPU Nvidia Tesla M60", fontsize=13.5)
plt.savefig('SpeedupVsThreads.png')

sizeN = [20400,82560,185760,330240,516000,743040,1320960,2064000]
etime = [2.18476,7.498288,26.764,77.167,179.900253,365.85,1134.63615,2773.71]

cpuN = [20600, 168300, 185800, 330200]
eN = [1.8, 124, 170, 537]



lsN = [np.log(itm) for itm in sizeN]
let = [np.log(itm) for itm in etime]

lsNN = [np.log(itm) for itm in cpuN]
letN = [np.log(itm) for itm in eN]

A = np.vstack([lsN[-4:], np.ones(len(lsN[-4:]))]).T
a,b = np.linalg.lstsq(A, let[-4:], rcond=None)[0]
AN = np.vstack([lsNN[-4:], np.ones(len(lsNN[-4:]))]).T
aN,bN = np.linalg.lstsq(AN, letN[-4:], rcond=None)[0]

xax = np.linspace(sizeN[0]-3000,sizeN[-1]+200000,200)
yay = [np.exp(a*np.log(itm)+b) for itm in xax]
yayN = [np.exp(aN*np.log(itm)+bN) for itm in xax]

fig, ax = plt.subplots(figsize = (8,6))
ax.loglog(xax,yay, '-', color='#07af1a',alpha=0.8, label = r"$ax+b$, with $a\simeq 1.97$")
ax.loglog(xax,yayN, '-', color='#4386f2',alpha=0.5)
ax.loglog(sizeN,etime, 'o', color='#bc0505',alpha=0.7, label="Datapoints")
ax.loglog(cpuN, eN, 'o', color = '#3e83f2', alpha=0.8, label='CPU')

plt.xlabel("Total number of pixels",fontsize=14)
plt.ylabel("Execution Time",fontsize=14)
plt.legend(loc='upper left', frameon=True, fancybox=True, facecolor='white', fontsize=14)
plt.xlim([sizeN[0]-3000,sizeN[-1]+200000])
plt.title("Execution time as a function of number of pixels, on a GPU Nvidia Tesla M60.")
plt.grid(which='both')
plt.savefig("EtimeGPU.png")
print("a=",a)
plt.show()
