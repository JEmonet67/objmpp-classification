#!/home/jerome/anaconda3/bin/python3

"""Written by Xavier Descombes, INRIA"""

import numpy as np
import imageio as io
from skimage import img_as_ubyte
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

def erode_ellipses(path_file, path_output):
    list_img = [f for f in listdir(path_file) if isfile(join(path_file, f))]
    dim = plt.imread(f"{path_file}/{list_img[0]}").shape
    somme = np.zeros([dim[0],dim[1]])
    
    for fichier in list_img:
        img_ellipse = plt.imread(f"{path_file}/{fichier}")
        img_ellipse[img_ellipse > 0.3] = 0
        img_ellipse[img_ellipse != 0] = 1
        somme += img_ellipse
        io.imwrite(f"{path_output}/{fichier}",img_as_ubyte(img_ellipse))
    
    io.imwrite(f"{path_output}/ALL_Ellipses.png",img_as_ubyte(somme))


    

path_file_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Exemple_type/local_map_GFP-01_w24-DAPI_TIF_2020y03m06d14h55m39s760l"
path_output_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Exemple_type/local_map_GFP-01_w24-DAPI_TIF_2020y03m06d14h55m39s760l/Ellipses_érodée"
erode_ellipses(path_file_t,path_output_t)