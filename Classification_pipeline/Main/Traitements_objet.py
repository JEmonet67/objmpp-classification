#!/home/jerome/anaconda3/bin/python3

"""Written by Jérôme Emonet"""

import numpy as np
import imageio as io
from skimage import img_as_ubyte
from os import listdir
from os.path import splitext
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.morphology import distance_transform_edt
import cv2 as cv

#Code pour binariser, éroder et fusionner les map des distances des objets.
def Erode_ellipses(path_file):
    list_img = [f for f in listdir(path_file) if ".npy" == splitext(f)[1]]
    dim = np.load(f"{path_file}/{list_img[0]}").shape
    All_ell_erod = np.zeros([dim[0],dim[1]])
    
    for fichier in list_img:
        img_ellipse = np.load(f"{path_file}/{fichier}")
        img_ellipse[img_ellipse > 0.3] = 0
        img_ellipse[img_ellipse != 0] = 1
        All_ell_erod += img_ellipse
    
    #io.imwrite(f"{path_file}/All_Ellipses_érodées.png",img_as_ubyte(somme))
    return All_ell_erod
    

path_file_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l"
#Erode_ellipses(path_file_t)

#Code pour binariser une image des régions.
def Binaryze_ellipses(path_regions):
    All_ell = np.copy(plt.imread(path_regions))
    All_ell[All_ell != 0] = 1
    #io.imwrite(f"{path_output}/All_Ellipses.png",img_as_ubyte(img))
    return All_ell


#Code pour séparer chaque ellipses à partir d'une image des régions.
def Separate_ellipses(regions, path_csv):
    df_marks = pd.read_csv(path_csv)
    list_center_y = df_marks["Center Col"]
    list_center_x = df_marks["Center Row"]
    list_region_obj = []
    
    for n_ell in range(1,len(list_center_x)+1):
        img = np.copy(regions)
        center_y = list_center_y[n_ell-1]
        center_x = list_center_x[n_ell-1]
        
        value_center = img[(center_x,center_y)]
        
        img[img != value_center] = 0
        img[img == value_center] = 255
        
        list_region_obj = list_region_obj + [img]
        # io.imwrite(f"{path_output}/Ellipse_{n_ell}.png", img)
        # np.save(f"{path_output}/Ellipse_{n_ell}.npy", img)
    
    return list_region_obj
    


path_output_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/Test_Results/Img_marker_watershed_segmentation"
path_csv_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/UBTD1-03_w24-DAPI_TIF-marks-2020y06m09d14h48m55s317l.csv"
path_regions_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/Test_Results/Labels_méthode_2.png"

#Separate_ellipses(path_output_t,path_regions_t,path_csv_t)


#Code pour créer une map de distance à partir d'un objet.
def Distance_map(path_file,list_obj):
    n_obj = 1
    list_dm_obj = []
    for obj in list_obj:
        dm_obj = distance_transform_edt(obj)
        list_dm_obj = list_dm_obj + [dm_obj]
        #np.save(f"{path_file}/local_map_watersh_{n_obj}.npy",dm_obj)
        dm_obj_norm = cv.normalize(dm_obj, np.zeros(dm_obj.shape),0, 255, cv.NORM_MINMAX)
        io.imwrite(f"{path_file}/local_map_watersh_{n_obj}.png",np.uint8(dm_obj_norm))
        n_obj += 1
    
    return list_dm_obj

path_file_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/Test_Results/Img_marker_watershed_segmentation"
#Distance_map(path_file_t)

