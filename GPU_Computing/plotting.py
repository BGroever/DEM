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
plt.show()
