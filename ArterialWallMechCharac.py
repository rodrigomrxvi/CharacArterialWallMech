## Script to obtain material constants of Arterial Wall based on Masson et al. 208 Journal of Biomechanics "Characterization of arterial wall mechanical behavior and stresses from human clinical data"
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve


### Read P(ext) File
expe={}
readFile = open("Pexpe.csv", 'r')
sepFile_nou = readFile.read().split('\n')
readFile.close()
columns = sepFile_nou[0].split(',')
print(columns)
len_x = len(columns)
ic = 0
for x in range(0,len_x):
    t1 = []
    for plotPair1 in sepFile_nou[1:]:
        xSTRING_1 = plotPair1.split(',')
        if len(xSTRING_1) > 1:
           t1.append(float(xSTRING_1[ic]))
    expe[columns[ic]]= t1
    ic = ic+1

###Function to compute pressure 

def Press_t(a,b,rm_td,rm,Int_ri_rm):
    Pa=a*np.exp(b*rm/rm_td)
    P=Pa+Int_ri_rm
    return P

def Integrate_sigma(sigma_theta,sigma_rr,r,lambda_r,c):
    sigma_rr=-p+c*lambda_r*lambda_r
