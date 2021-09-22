import json                                 #Para leer archivos json -> dict{}
import matplotlib.pyplot as plt             #Para gráficar
import cv2                                  #OpenCV - visión computacional
import numpy as np                          #Álgebra lineal
import imageio                              #Generar el GIF

def load(file: str) :                       #Convertir el json en dict
    with open(file) as json_file:
        db = json.load(json_file)
        json_file.close()
        return db

def animate(r, time, name):
    figure, axes = plt.subplots()
    limit = 6
    d_arteria = plt.Circle((0.0, 0.0), r, lw=10, fill=False, color=(0.8,0.4,0.4))
    axes.set_aspect(1)
    axes.add_artist(d_arteria)
    plt.xlim(-limit,limit)
    plt.ylim(-limit,limit)
    plt.xlabel("(mm)")
    plt.ylabel("(mm)")
    plt.title("Time: "+str(time)+" (s)")
    plt.savefig(name)

def images(r, time, img, name):
    d=r*2
    fondo = 255*np.ones((820,1200,3),dtype=np.uint8)      #Generamos el fondo blanco 820x1200px
    img   = cv2.resize(img,None,fx=d,fy=d,interpolation=cv2.INTER_CUBIC) #aplicamos zoom
    font = cv2.FONT_HERSHEY_SIMPLEX                       #Configuramos fuentes
    cv2.putText(fondo,'Tiempo: '+str(time)+" (s)",(10,30),font,1,(10,10,10),2,cv2.LINE_AA)  #Escribimos el tiempo en la imagen
    x_offset= int(((fondo.shape[1]-img.shape[1])/2))   #Calcular el centro de la imagen
    y_offset= int(((fondo.shape[0]-img.shape[0])/2))
    cv2.putText(fondo,'Diametro: '+str(d)+" (mm)",(10,810),font,1,(10,10,10),2,cv2.LINE_AA) #Escribimos el diametro en la imágen
    
    fondo[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img  #Superponemos la imagen de la arteria en el fondo
    #cv2.imshow('imagen',fondo)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print("Fondo: ",fondo.shape)
    # print("Imagen:",img.shape)
    # print(x_offset,y_offset)
    cv2.imwrite(name, cv2.cvtColor(fondo, cv2.COLOR_RGB2BGR))
    return fondo

def createGIF(frames, name):
    with imageio.get_writer(name+".gif", mode="I") as writer:
        for idx, frame in enumerate(frames):
            writer.append_data(frame)
        writer.close()
print("Hola")
#Lectura de imagen 
img = cv2.imread("arteria.jpg")  #  numpy -> [[b],[g],[r]]
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #  numpy -> [[r],[g],[b]]

datos = load("animation.json")      #Leemos el json

gifImage = []                       #Lista que almacenará los frames a animar

for i, diam in enumerate(datos["diametro"][5:95]):
    try:
        gifImage.append(images((diam*8.52)/2, datos["time"][i+5], img, "./frameImage/frame"+str(i+1)+".jpg"))
        # gifFrame.append(animate((diam*8.52)/2, datos["time"][i], "./frames/frame"+str(i+1)+".jpg"))
    except:
        None

gifImage = np.array(gifImage)
createGIF(gifImage,"Arteria1")