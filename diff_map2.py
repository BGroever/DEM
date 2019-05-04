#!/usr/bin/python
import numpy as np
from math import *
from skimage import io
import matplotlib.pyplot as plt
import sys

# Read in the color values for each state
b=open("colchart.txt","r")
c={}
d=[0 for i in range(51)]
ind={}
k=0
for l in b:
    a=l.split()

    # Read in the three color channels
    re=int(a[0])
    gr=int(a[1])
    bl=int(a[2])

    # Read in the name of the state, taking care to handle to states with a
    # space in them
    if(len(a)==4):
        na=a[3]
    else:
        na=a[3]+" "+a[4]

    # Encode the color into a single integer, and store the information
    nu=re+256*gr+65536*bl
    c[nu]=k
    ind[na]=k
    d[k]=nu
    k+=1
b.close()

# Read in the population densities for each state
rh=[0. for i in range(51)]
b=open("density.txt","r")
for l in b:
    a=l.split()
    if(len(a)==2):
        na=a[1]
    else:
        na=a[1]+" "+a[2]
    rh[ind[na]]=float(a[0])
b.close()

# Read in the undeformed US map
o=io.imread("usa_vs.png")
(m,n,z)=o.shape

# Grid spacing
h=1.
ih2=0.5/h

# Scan the image to set the density field in the states. In addition, calculate
# the average density.
u=np.zeros((m,n))
cu=np.zeros((m,n))
srho=0.
npts=0
for i in range(m):
    for j in range(n):
        co=o[i,j,0]+256*o[i,j,1]+65536*o[i,j,2]
        if co in c:
            u[i,j]=rh[c[co]]
            srho+=u[i,j];npts+=1
        elif co!=16777215:
            sys.exit()

# Re-scan over the image to set the average density in regions outside the
# states
rhobar=srho/npts
print("Avg. rho",rhobar)
for i in range(m):
    for j in range(n):
        co=o[i,j,0]+256*o[i,j,1]+65536*o[i,j,2]
        if co==16777215:
            u[i,j]=rhobar

# Initialize the reference map coordinates
X=np.zeros((m,n,2))
cX=np.zeros((m,n,2))
for i in range(m):
    for j in range(n):
        X[i,j,0]=h*i
        X[i,j,1]=h*j

# Calculate timestep size
dt=0.24*h*h
T=(m*m+n*n)/12.
nsteps=int(ceil(T/dt))
dt=T/nsteps
print("Solving to T =",T,"using",nsteps,"timesteps")

# Function to integrate the density and reference map fields forward in time by
# dt
def step(dt):
    global time,u,cu,X,cX
    nu=dt/(h*h)
    fac=ih2*dt/h
    maxvsq=0.

    # Calculate the upwinded update for the reference map
    for i in range(m):
        for j in range(n):
            if i>0 and i<m-1:
                vx=-(u[i+1,j]-u[i-1,j])*fac/u[i,j]
                if vx>0:
                        cX[i,j,:]=vx*(-X[i,j,:]+X[i-1,j,:])
                else:
                        cX[i,j,:]=vx*(X[i,j,:]-X[i+1,j,:])
            else:
                cX[i,j,:]=0.

            if j>0 and j<n-1:
                vy=-(u[i,j+1]-u[i,j-1])*fac/u[i,j]
                if vy>0:
                        cX[i,j,:]+=vy*(-X[i,j,:]+X[i,j-1,:])
                else:
                        cX[i,j,:]+=vy*(X[i,j,:]-X[i,j+1,:])
    X+=cX

    # Do the finite-difference update
    for i in range(m):
        for j in range(n):
            if i>0: tem=u[i-1,j];k=1
            else: tem=0;k=0
            if j>0: tem+=u[i,j-1];k+=1
            if j<n-1: tem+=u[i,j+1];k+=1
            if i<m-1: tem+=u[i+1,j];k+=1
            cu[i,j]=tem-k*u[i,j]
    u+=cu*nu

    # Print the current time and the extremal values of density
    time+=dt
    #print(time,np.min(u),np.max(u))

# Perform the integration timesteps, using the smaller dt for the first few
# steps to deal with the large velocities that initially occur
time=0
for l in range(24):
    step(dt/24.)
for l in range(1,nsteps):
    step(dt)

# Use the deformed reference map to plot the density-equalized US map
o2=np.empty((m,n,z),dtype=np.uint8)
for i in range(m):
    for j in range(n):
        i2=int(X[i,j,0]+0.5)
        j2=int(X[i,j,1]+0.5)
        if i2<0: i2=0
        elif i2>m-1: i2=m-1
        if j2<0: j2=0
        elif j2>n-1: j2=n-1
        o2[i,j,:]=o[i2,j2,:]
io.imsave("dens_eq.png",o2)

# Plot the deformed reference map
xx=np.linspace(m-1,0.,m)
yy=np.linspace(0.,n-1,n)
XX,YY=np.meshgrid(yy,xx)
plt.contourf(XX, YY, u, 16, alpha=.75)
plt.contour(XX, YY, X[:,:,0], 16, colors='black', linewidth=.5)
plt.contour(XX, YY, X[:,:,1], 16, colors='black', linewidth=.5)
plt.show()
