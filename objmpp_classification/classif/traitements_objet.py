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
def Erode_ellipses(list_distmap,path_file=False):
    dim = list_distmap[0].shape
    All_ell_erod = np.zeros([dim[0],dim[1]])
    
    for distmap_ell in list_distmap:
        distmap_ell_norm = cv.normalize(distmap_ell, np.zeros(distmap_ell.shape),0,1,cv.NORM_MINMAX)
        distmap_ell_norm[distmap_ell_norm < 0.7] = 0
        distmap_ell_norm[distmap_ell_norm != 0] = 1
        All_ell_erod += distmap_ell_norm
    
    if path_file != False:
        All_ell_erod_norm = cv.normalize(All_ell_erod, np.zeros(All_ell_erod.shape),0, 255, cv.NORM_MINMAX)
        io.imwrite(f"{path_file}/All_Ellipses_érodées.png",np.uint8(All_ell_erod_norm))
        
    return All_ell_erod
    

# path_file_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l"
# Erode_ellipses(path_file_t)

#Code pour binariser une image des régions.
def Binaryze_ellipses(path_regions):
    All_ell = np.copy(plt.imread(path_regions))
    All_ell[All_ell != 0] = 1
    #io.imwrite(f"{path_output}/All_Ellipses.png",img_as_ubyte(img))
    return All_ell

def Dilate_ellipses(list_ells_sep):
    dim = list_ells_sep[0].shape
    all_ells_dilated = np.zeros([dim[0],dim[1]])
    kernel = np.ones((5,5), np.uint8) 
    
    for ells in list_ells_sep:
        all_ells_dilated = all_ells_dilated + cv.dilate(ells,kernel, iterations=4)
    
    all_ells_dilated[all_ells_dilated!=0] = 255
    all_ells_dilated = cv.normalize(all_ells_dilated, np.zeros(all_ells_dilated.shape),0, 1, cv.NORM_MINMAX)
    all_ells_dilated = np.float32(all_ells_dilated)
    return all_ells_dilated 

#Code pour séparer chaque ellipses à partir d'une image des régions.
def Separate_ellipses(img_all_regions):
    list_region_sep = []
    list_objects = [objets for objets in np.unique(img_all_regions) if objets!=0]
    for value_obj in list_objects:
        img_region = np.copy(img_all_regions)
        img_region[img_region != value_obj] = 0
        img_region[img_region == value_obj] = 255
        
        list_region_sep = list_region_sep + [img_region]
        # io.imwrite(f"{path_output}/Ellipse_{n_ell}.png", img_region)
        # np.save(f"{path_output}/Ellipse_{n_ell}.npy", img_region)
    
    return list_region_sep
  
def Separate_ells_watershed(regions, path_csv,path_output=False):
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
        
        if path_output!=False:
            io.imwrite(f"{path_output}/Ellipse_{n_ell}.png", img)
            np.save(f"{path_output}/Ellipse_{n_ell}.npy", img)
    
    return list_region_obj

# path_output_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/Test_Results/Img_marker_watershed_segmentation"
# path_csv_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/UBTD1-03_w24-DAPI_TIF-marks-2020y06m09d14h48m55s317l.csv"
# path_regions_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/Images_KO/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/Test_Results/Labels_méthode_2.png"

# Separate_ellipses(path_output_t,path_regions_t,path_csv_t)


#Code pour créer une map de distance à partir d'un objet.
def Distance_map(list_obj,path_file=False):
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
            np.save(f"{path_file}/local_map_watersh_{n_obj}.npy",dm_obj_int8)
        n_obj += 1
    return list_dm_obj



# path_file_t = "/home/jerome/Bureau/Img"
# fi = open('/home/jerome/Bureau/Test/local_map_UBTD1-03_w24-DAPI_TIF_2020y06m09d14h48m55s317l/local_map_watershed/Liste_regions_objets.txt','rb')
# list_obj_t = pickle.Unpickler(fi2).load()
# Distance_map(path_file_t,list_obj_t)