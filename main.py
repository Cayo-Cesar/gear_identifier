import cv2
import numpy as np


img = cv2.imread('images/imagem0.jpeg')
img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, threshold = cv2.threshold(img_cinza, 127, 255, cv2.THRESH_BINARY)
img1 = cv2.bitwise_not(threshold)

contornos, _ = cv2.findContours(img1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

limiteInferior = 20771.0
limiteSuperior = 20786.5

objetos = []
objetos1 = []

areaseq = []
lista_ordenada = []
 
for i in contornos:
    area = cv2.contourArea(i) 
    areaseq.append(area)
 
lista_ordenada = sorted(areaseq)
 
for i in contornos:
    area = cv2.contourArea(i)
    print(area)    
    if  ((area >= limiteInferior ) and (area <= limiteSuperior)) :  
        objetos.append(i)
    elif area > 1000:
        objetos1.append(i)      

mask = np.zeros_like(threshold)

img2 = cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_REPLICATE)

img_contornos = cv2.drawContours(img, objetos, -1 , (255, 0, 0), 2)

cv2.imshow("engrenagens aceitas", img_contornos)
cv2.imwrite("engrenagens aceitas.png", img_contornos)

img_contornos1 = cv2.drawContours(img2, objetos1, -1 , (0, 0, 255), 2)

cv2.imshow("engrenagens recusadas", img_contornos1)
cv2.imwrite("engrenagens recusadas.png", img_contornos1)

img_contornos = cv2.drawContours(img, objetos1, -1 , (0, 0, 255), 2)

cv2.imshow("aceitas e recusadas", img)
cv2.imwrite("aceitas e recusadas.png", img)

img_contornos = cv2.drawContours(mask, objetos, -1, 255, -1)

background = np.full_like(img, (255, 255, 255))

object_in_background = np.zeros_like(img)
object_in_background[mask == 255] = img[mask == 255]

img[mask == 255] = background[mask == 255]
img[mask != 255] = object_in_background[mask != 255]

img = cv2.bitwise_not(img)
cv2.imshow('Engrenagens corretas', img)
cv2.imwrite('Engrenagens corretas.png', img) 
 
cv2.waitKey(0)