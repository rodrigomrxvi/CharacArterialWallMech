import numpy as np                                   #Biblioteca para realizar operaciones de álgebra lineal
import matplotlib.pyplot as plt                      #Gráficar funciones
import scipy.integrate as integrate                  #Biblioteca para realizar operaciones de cálculo
from scipy.interpolate import pchip_interpolate
import csv                                           #Herramienta que nos ayuda a leer archivos de texto CSV
import os                                            #Biblioteca te ayuda a realizar operaciones que se ejecutan directamente en el SO donde se esté ejecutando
import sys                                           #Herramientas del sistema
import json

# Read data from paper
file1='PatientADiameter.csv'                         #Nombres de las Bases de Datos a utilizar  
file2='PatientAPressure.csv'

readFile = open(file1,'r')                           #Abrimos 'file1' como lectura
sepFile_nou = readFile.read().split('\n')            #Obtenemos una lista con cada linea del archivo leído
readFile.close()                                     #Cerramos la lectura de 'file1'
time=[]                                              #Inicializando una lista vacia
diam=[]
for elements in sepFile_nou:                         #Indexamos cada linea leida en 'file1' en 'elements'
    xSTRING_1 = elements.split(',')                  #Dividimos la linea por comas (Columnas)  [0.01214882308276384, 0.022099447513812098]
    # print(xSTRING_1)
    if len(xSTRING_1) > 1:                           #Nos aseguramos de que existan 2 columnas en esta linea
        time.append(float(xSTRING_1[0]))             #Convertimos la columna 1 a flotante y la agregamos a la lista de tiempo
        diam.append(float(xSTRING_1[1]))             #Convertimos la columna 2 a flotante y la agregamos a la lista de diemetro 

readFile = open(file2,'r')                           #Repetimos el proceso de 'file1' para 'file2'
sepFile_nou = readFile.read().split('\n')
readFile.close()
time1=[]
pressure=[]
for elements in sepFile_nou:
    xSTRING_1 = elements.split(',')
    # print(xSTRING_1)
    if len(xSTRING_1) > 1:
        time1.append(float(xSTRING_1[0]))
        pressure.append(float(xSTRING_1[1]))         #Termina operación para 'file2'

#Interpolate to have equidistant time steps
time_interpolation = np.linspace(min(time), max(time), num=100)                           #Generamos un espacio lineal de Ti a Tf en 100 pasos
diam_interpolation = pchip_interpolate(time,diam,time_interpolation)                      #Generamos la curva que une a todas las mediciones del diametro
pressure_interpolation = pchip_interpolate(time1,pressure,time_interpolation)             #Generamos la curva que une a todas las mediciones de la presión

#Starts plot configuration
font = {'family' : 'serif',                     #Genera un dicado con las características de la fuente que se va a mostrar en la gŕafica            
        'weight' : 'medium',
        'size'   : 34}

plt.rc('font', **font)                                                                          #Configuramos la fuente para matplotlib
plt.plot(time,diam,"o",markersize=6,label="Diameter Masson et al.")                             #Gráfica del diametro-tiempo                                
plt.plot(time_interpolation,diam_interpolation,linewidth=3,label="Diameter interpolation")      #Gráfica del diametro_interpolation-tiempo
plt.plot(time1,pressure,"x",markersize=6,label="Pressure Masson et al.")                        #Gráfica de presión-tiempo
plt.plot(time_interpolation,pressure_interpolation,linewidth=3,label="Pressure interpolation")  #Gráfica de interpolacion de la presión-tiempo
plt.xlabel('Normalized time')                                         #Etiqueta a el frame de la gráfica en x
plt.ylabel('Normalized diameter/pressure)')                           #Etiqueta para el eje y
plt.legend()                                                          #Mostramos las leyendas correspondientes a cada gráfica
plt.show()                                                            #Mostramos la gráfica creada

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
rm=r+r*0.005             ## In the paper they say the measured the rm however they do not report it, thus we consider the thicknes as 5% of r
R=Referenceradi(Rm,lambdaP,Lambda,Thetazero,rm)
lambdatheta=eigentheta(r,Thetazero,R)
print(lambdatheta) 

animate = {"diametro":list(diam_interpolation), "presion": list(pressure_interpolation),"time":list(time_interpolation)}
with open("animation.json", 'w') as outfile:
    json.dump(animate, outfile)
    outfile.close()


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
