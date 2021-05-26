import numpy as np 
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.interpolate import pchip_interpolate
import csv
import os
import sys

# Read data from paper
file1='PatientADiameter.csv'
file2='PatientAPressure.csv'

readFile = open(file1,'r')
sepFile_nou = readFile.read().split('\n')
readFile.close()
time=[]
diam=[]
for elements in sepFile_nou:
    xSTRING_1 = elements.split(',')
    print(xSTRING_1)
    if len(xSTRING_1) > 1:
        time.append(float(xSTRING_1[0]))
        diam.append(float(xSTRING_1[1]))

readFile = open(file2,'r')
sepFile_nou = readFile.read().split('\n')
readFile.close()
time1=[]
pressure=[]
for elements in sepFile_nou:
    xSTRING_1 = elements.split(',')
    print(xSTRING_1)
    if len(xSTRING_1) > 1:
        time1.append(float(xSTRING_1[0]))
        pressure.append(float(xSTRING_1[1]))

#Interpolate to have equidistant time steps
time_interpolation = np.linspace(min(time), max(time), num=100)
diam_interpolation = pchip_interpolate(time,diam,time_interpolation)
pressure_interpolation = pchip_interpolate(time1,pressure,time_interpolation)

font = {'family' : 'serif',
        'weight' : 'medium',
        'size'   : 34}
plt.rc('font', **font)
plt.plot(time,diam,"o",markersize=6,label="Diameter Masson et al.")
plt.plot(time_interpolation,diam_interpolation,linewidth=3,label="Diameter interpolation")
plt.plot(time1,pressure,"x",markersize=6,label="Pressure Masson et al.")
plt.plot(time_interpolation,pressure_interpolation,linewidth=3,label="Pressure interpolation")
plt.xlabel('Normalized time')
plt.ylabel('Normalized diameter/pressure)')
plt.legend()
plt.show()

#Material Parameters
Rm= 4.26 #mm
Thetazero=np.radians(128.7) ## In deg
lambdaP= 1.11
c=29.82e3
c1=9.45e3
c2=14.14
c1circ=16.13e3
c2circ=15.11
alpha=np.radians(65.7)
Tm=39.73e3
lambdazero=0.96
lambdam=1.7
a=0.12e3
b=3.52

#Assumptions
Lambda=1.0
lambdaz=lambdaP*Lambda

#Functions
def Referenceradi(Rm,lambdaP,Lambda,Thetazero,rm):
    R=np.sqrt(Rm**2-(np.pi*lambdaP*Lambda/Thetazero*(rm**2-r**2)))
    return R
def eigentheta(r,Thetazero,R):
    lambdatheta=np.pi*r/(Thetazero*R)
    return lambdatheta
#Computations
r=diam_interpolation/2.0 ## This is the interpolated experimental inner radi
rm=r+r*0.005 ## In the paper they say the measured the rm however they do not report it, thus we consider the thicknes as 5% of r
R=Referenceradi(Rm,lambdaP,Lambda,Thetazero,rm)
lambdatheta=eigentheta(r,Thetazero,R)
print(lambdatheta) 

### Vectors
#c1vec=np.array([c1,c1circ,c1,c1])
#c2vec=np.array([c2,c2circ,c2,c2])
#alphak=np.array([0,np.pi/2,alpha,-alpha]) ## This is in degrees we need to check if it should be Pi/2
#lambdak=lambdatheta**2*sin(alphak)**2+lambdaz**2*cos(alphak)**2
#
#def (lambda) :
#    T1=c*(lambdatheta**2-lambdaz**2)
#    T2=lambdatheta**2*np.sum(c1vec*((lambdak**2)-1)*np.exp(c2vec*((lambdak**2)-1)**2*)*(sin(alphak)**2))
#    T3=
#    T4=
#    simgatt_sigmarr=T1+T2+T3-T4
#    #Int = scypy.int((sigmatt-sigmarr)/r,r)
#    #pa = a*np.exp(b*(rm/rm_td))
#    #pi = pa + Int

#error = pi-pexp
