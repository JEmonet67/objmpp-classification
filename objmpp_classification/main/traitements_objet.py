#!/home/jerome/anaconda3/bin/python3

"""Written by Jérôme Emonet"""

import numpy as np
import imageio as io
from os import listdir
from os.path import splitext
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import cv2 as cv
import pickle

#Code pour binariser, éroder et fusionner les map des distances des objets.
def Erode_ellipses(list_distmap,path_file):
    dim = list_distmap[0].shape
    All_ell_erod = np.zeros([dim[0],dim[1]])
    
    for distmap_ell in list_distmap:
        distmap_ell[distmap_ell > 0.3] = 0
        distmap_ell[distmap_ell != 0] = 1
        All_ell_erod += distmap_ell
    
    io.imwrite(f"{path_file}/All_Ellipses_érodées.png",img_as_ubyte(somme))
    return All_ell_erod
    

# path_file_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l"
# Erode_ellipses(path_file_t)

#Code pour binariser une image des régions.
def Binaryze_ellipses(path_regions):
    All_ell = np.copy(plt.imread(path_regions))
    All_ell[All_ell != 0] = 1
    #io.imwrite(f"{path_output}/All_Ellipses.png",img_as_ubyte(img))
    return All_ell


#Code pour séparer chaque ellipses à partir d'une image des régions.
def Separate_ellipses(regions):
    list_region_sep = []
    img_all_regions = cv.imread(regions,0)
    list_objects = [objets for objets in np.unique(img_all_regions) if objets!=0]
    for value_obj in list_objects:
        img_region = np.copy(img_all_regions)
        img_region[img_region != value_obj] = 0
        img_region[img_region == value_obj] = 255
        
        list_region_sep = list_region_sep + [img_region]
        # io.imwrite(f"{path_output}/Ellipse_{n_ell}.png", img_region)
        # np.save(f"{path_output}/Ellipse_{n_ell}.npy", img_region)
    
    return list_region_sep
    


# path_output_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/Test_Results/Img_marker_watershed_segmentation"
# path_csv_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/UBTD1-03_w24-DAPI_TIF-marks-2020y06m09d14h48m55s317l.csv"
# path_regions_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/Test_Results/Labels_méthode_2.png"

# Separate_ellipses(path_output_t,path_regions_t,path_csv_t)


#Code pour créer une map de distance à partir d'un objet.
def Distance_map(path_file,list_obj):
    n_obj = 1
    list_dm_obj = []
    for obj in list_obj:
        obj_norm = cv.normalize(obj, np.zeros(obj.shape),0, 255, cv.NORM_MINMAX)
        obj_int8 = np.uint8(obj_norm)
        dm_obj = cv.distanceTransform(obj_int8, cv.DIST_L2, 3)
        dm_obj_norm = cv.normalize(dm_obj, np.zeros(dm_obj.shape),0, 255, cv.NORM_MINMAX)
        dm_obj_int8 = np.uint8(dm_obj_norm)
        list_dm_obj = list_dm_obj + [dm_obj_int8]
        if path_file != False:
            io.imwrite(f"{path_file}/local_map_watersh_{n_obj}.png",dm_obj_int8)
        n_obj += 1
    return list_dm_obj

# # check=False
# path_file_1 = "/home/jerome/Bureau/Img"
# fi1 = open('/home/jerome/Bureau/Test/local_map_UBTD1-01_w24-DAPI_TIF_2020y06m09d13h45m26s565l/local_map_watershed/Liste_regions_objets.txt','rb')
# list_obj_1 = pickle.Unpickler(fi1).load()
# liste, check = Distance_map(path_file_1,list_obj_1)

# if check == True:
#     path_file_2 = "/home/jerome/Bureau/Img"
#     fi2 = open('/home/jerome/Bureau/Test/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/local_map_watershed/Liste_regions_objets.txt','rb')
#     list_obj_2 = pickle.Unpickler(fi2).load()
#     Distance_map(path_file_2,list_obj_2)