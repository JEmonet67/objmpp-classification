#!/home/jerome/anaconda3/bin/python3

"""Written by Xavier Descombes, INRIA"""

import numpy as np
import imageio as io
from skimage import img_as_ubyte
from os import listdir
from os.path import splitext
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.morphology import distance_transform_edt

def erode_ellipses(path_file):
    list_img = [f for f in listdir(path_file) if ".npy" in splitext(f)[1]]
    dim = np.load(f"{path_file}/{list_img[0]}").shape
    somme = np.zeros([dim[0],dim[1]])
    
    for fichier in list_img:
        img_ellipse = np.load(f"{path_file}/{fichier}")
        img_ellipse[img_ellipse > 0.3] = 0
        img_ellipse[img_ellipse != 0] = 1
        somme += img_ellipse
    
    io.imwrite(f"{path_file}/All_Ellipses_érodées.png",img_as_ubyte(somme))
    

# path_file_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Test/Test_organoïde_trié_V2"
# erode_ellipses(path_file_t)


def Separate_ellipses(path_output,path_regions, path_csv):
    df_marks = pd.read_csv(path_csv)
    list_center_y = df_marks["Center Col"]
    list_center_x = df_marks["Center Row"]    
    
    for n_ell in range(1,len(list_center_x)+1):
        img = np.copy(plt.imread(path_regions))
        center_y = list_center_y[n_ell-1]
        center_x = list_center_x[n_ell-1]
        
        value_center = img[(center_x,center_y)]
        print(value_center)
        
        img[img != value_center] = 0
        img[img == value_center] = 255
        
        io.imwrite(f"{path_output}/Ellipse_{n_ell}.png", img)
        np.save(f"{path_output}/Ellipse_{n_ell}.npy", img)
    


# path_output_t = "/home/jerome/Stage_Classif_Organoid/Img_marker_watershed_segmentation"
# path_csv_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Exemple_type/GFP-01_w24-DAPI_TIF-marks-2020y03m06d14h55m39s760l.csv"
# path_regions_t = "/home/jerome/Stage_Classif_Organoid/Img_marker_watershed_segmentation/Regions_sementation_Xavier.tif"

# Separate_ellipses(path_output_t,path_regions_t,path_csv_t)



def distance_map(path_file):
    list_img = [f for f in listdir(path_file) if ".npy" in splitext(f)[1]]
    
    for name_img in list_img:
        arr_img = np.load(f"{path_file}/{name_img}")
        dm_img = distance_transform_edt(arr_img)
        np.save(f"{path_file}/local_map_GFP-01_w24-DAPI_TIF/{name_img}",dm_img)
        io.imwrite(f"{path_file}/local_map_GFP-01_w24-DAPI_TIF/{splitext(name_img)[0]}.png",dm_img)

path_file_t = "/home/jerome/Stage_Classif_Organoid/Img_marker_watershed_segmentation"

distance_map(path_file_t)