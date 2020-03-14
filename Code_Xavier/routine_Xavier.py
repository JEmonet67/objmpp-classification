#!/home/jerome/anaconda3/bin/python3

"""Written by Xavier Descombes, INRIA"""

import numpy as np
import math
import imageio as io
import matplotlib.pyplot as plt
from skimage import img_as_ubyte



def estim(ordre1,ordre2,nombre,est):
    
    if est==1:
        x_max = 1
        y_max = nombre[0]
    #Peut-être mettre 0 au lieu de 1 ici.
    
        for x in range(1,256):
            if y_max < nombre[x]:
                y_max = nombre[x]
                x_max = x
        
        x = x_max
        if nombre[x] != 0:
            varcond = ordre2[x]/nombre[x] - (ordre1[x]*ordre1[x])/(nombre[x]*nombre[x])
        else:
            varcond = 0
    
    else:
        varcond=0
        somme=0
        
        for x in range(1,256):
            if nombre[x] != 0:
                varcond = varcond + ordre2[x] - (ordre1[x]*ordre1[x]/nombre[x]*nombre[x])
                somme = somme + nombre[x]
        
        varcond = varcond/somme
    return float(varcond)



def VarCond(dep,taille,est):
    
    dim = dep.shape
    offset = int((taille-1)/2)
    
    # Initialisation
    
    tempe = np.array(np.zeros((dim[0],dim[1])), dtype="int64")
    voisin = np.array(np.zeros((dim[0],dim[1])), dtype="int64")
    carre = np.array(np.around(dep,2)*np.around(dep,2), dtype="int64")
    moy = np.array(np.zeros((256,1)), dtype="int64")
    var = np.array(np.zeros((256,1)), dtype="int64")
    num = np.array(np.zeros((256,1)), dtype="int64")
    
    # Calcul de la moyenne des voisins en chaque point
    dep = np.array(np.around(dep,2), dtype="int64")
    
    for i in range(1,dim[0]-2):
        for j in range(1,dim[1]-2):
            voisin[i,j] = 1 + (dep[i-1,j]+dep[i+1,j]+dep[i,j-1]+dep[i,j+1])/4
            # +1 pour passer de [0,255] à [1,256]
    
    voisin[0,0] = 1 + (dep[1,0]+dep[0,1])/2
    for j in range(1,dim[1]-2):
        voisin[0,j] = 1 + (dep[0,j-1]+dep[0,j+1]+dep[i+1,j])/3
    
    voisin[0,dim[1]-1] = 1 + (dep[0,dim[1]-2]+dep[1,dim[1]-1])/2
    for i in range(1,dim[0]-2):
        voisin[i,0] = 1 + (dep[i-1,0]+dep[i+1,0]+dep[i,1])/3
        voisin[i,dim[1]-1] = 1 + (dep[i-1,dim[1]-1]+dep[i+1,dim[1]-1] + dep[i,dim[1]-2])/3
    
    voisin[dim[0]-1,0] = 1 + (dep[dim[0]-2,0]+dep[dim[0]-1,1])/2
    for j in range(1,dim[1]-2):
        voisin[dim[0]-1,j] = 1 + (dep[dim[0]-1,j-1]+dep[dim[0]-1,j+1]+dep[dim[0]-2,j])/3
    
    voisin[dim[0]-1,dim[1]-1] = 1 + (dep[dim[0]-1,dim[1]-2]+ dep[dim[0]-2,dim[1]-2])/2
        
    for i in range(0,dim[0]):
        print("Initialisation it",i)
        for j in range(0,dim[1]):
            voisin[i,j] = int(math.floor(voisin[i,j]))
    
        # Procédure de la fenêtre glissante
    
        # Initialisation
    
        for i in range(0,taille):
            for j in range(0,taille):
                num[voisin[i,j]] = num[voisin[i,j]] + 1
                moy[voisin[i,j]] = moy[voisin[i,j]] + np.around(dep[i,j],2)
                var[voisin[i,j]] = var[voisin[i,j]] + np.around(carre[i,j],2)

                
        # for i in range(0,taille):
        #     for j in range(0,taille):
        #         num[int(voisin[i,j])] = num[int(voisin[i,j])] + 1
        #         moy[int(voisin[i,j])] = moy[int(voisin[i,j])] + np.around(dep[i,j],2)
        #         var[int(voisin[i,j])] = var[int(voisin[i,j])] + np.around(carre[i,j],2)
    
    # np.save(path_tests + "Var", var)
    # np.save(path_tests + "Moy", moy)
    # np.save(path_tests + "num", num)
    # np.save(path_tests + "est", est)
    
    tempe[offset+1,offset+1] = 1
    
    
    for i in range(offset+1,dim[1]-1-offset,2):
        print("Algorithme, it",i)
        for j in range(offset+2,dim[1]-1-offset):
            for k in range(-offset,offset):
                
                di = i+k
                dj = j-offset-1
                num[voisin[di,dj]] = num[voisin[di,dj]] - 1
                moy[voisin[di,dj]] = moy[voisin[di,dj]] - np.around(dep[di,dj],2)
                var[voisin[di,dj]] = var[voisin[di,dj]] - np.around(carre[di,dj],2)
                dj = j+offset
                num[voisin[di,dj]] = num[voisin[di,dj]] + 1
                moy[voisin[di,dj]] = moy[voisin[di,dj]] + np.around(dep[di,dj],2)
                var[voisin[di,dj]] = var[voisin[di,dj]] + np.around(carre[di,dj],2)
            
            tempe[i,j] = estim(moy,var,num,est)
            
        # Changement de ligne
        
        for k in range(-offset,offset):
            di = i-offset
            dj = dim[1]-1-offset+k
            num[voisin[di,dj]] = num[voisin[di,dj]] - 1
            moy[voisin[di,dj]] = moy[voisin[di,dj]] - np.around(dep[di,dj],2)
            var[voisin[di,dj]] = var[voisin[di,dj]] - np.around(carre[di,dj],2)
            di = i+1+offset
            num[voisin[di,dj]] = num[voisin[di,dj]] + 1
            moy[voisin[di,dj]] = moy[voisin[di,dj]] + np.around(dep[di,dj],2)
            var[voisin[di,dj]] = var[voisin[di,dj]] + np.around(carre[di,dj],2)
        
        tempe[i+1,dim[1]-offset] = estim(moy,var,num,est)
        
        
        # Ligne i+1 : de droite à gauche
        
        for j in range(dim[1]-offset-2,offset+1,-1):
            for k in range(-offset,offset):
                
                di = i+1+k
                dj = j+offset+1
                num[voisin[di,dj]] = num[voisin[di,dj]] - 1
                moy[voisin[di,dj]] = moy[voisin[di,dj]] - np.around(dep[di,dj],2)
                var[voisin[di,dj]] = var[voisin[di,dj]] - np.around(carre[di,dj],2)
                dj = j-offset
                num[voisin[di,dj]] = num[voisin[di,dj]] + 1
                moy[voisin[di,dj]] = moy[voisin[di,dj]] + np.around(dep[di,dj],2)
                var[voisin[di,dj]] = var[voisin[di,dj]] + np.around(carre[di,dj],2)
            
            tempe[i+1,j]=estim(moy,var,num,est)
        
        
        # Changement de ligne
        
        if i!=dim[0]-offset-1:
            for k in range(-offset,offset):
                di = i+1-offset
                dj = offset+1+k
                num[voisin[di,dj]] = num[voisin[di,dj]] - 1
                moy[voisin[di,dj]] = moy[voisin[di,dj]] - np.around(dep[di,dj],2)
                var[voisin[di,dj]] = var[voisin[di,dj]] - np.around(carre[di,dj],2)
                di = i+2+offset
                num[voisin[di,dj]] = num[voisin[di,dj]] + 1
                moy[voisin[di,dj]] = moy[voisin[di,dj]] + np.around(dep[di,dj],2)
                var[voisin[di,dj]] = var[voisin[di,dj]] + np.around(carre[di,dj],2)
                    
    # Affichage du paramètre de texture
    
    # io.imshow(max(tempe/(range(dep,2)+0.1),0))
    
    print("Dernier point de contrôle")
    
    return tempe

dep_t = plt.imread("/home/jerome/Stage_Classif_Organoid/Image_Organoïdes/Images_transformées/GFP-01_w24-DAPI.tif")
dep_t = dep_t[0:500,0:500]
taille_t = 15
est_t = 1

img = VarCond(dep_t,taille_t,est_t)
path_tests = "/home/jerome/Stage_Classif_Organoid/Image_Organoïdes/Images_transformées/Img_Code_Xavier/"
io.imwrite(path_tests + "Img500.png",dep_t)
np.save(path_tests + "VarCond.npy", img)
io.imwrite(path_tests + "VarCond.png", img_as_ubyte(img))


