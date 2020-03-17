#!/home/jerome/anaconda3/bin/python3

#Importation des modules.
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import imageio as io
from skimage import img_as_ubyte
import pandas as pd


    
def Correspondance_ellipses(path_regions_mpp,path_regions_watersh, path_csv):
    df_marks = pd.read_csv(path_csv)
    list_center_x = df_marks["Center Col"]
    list_center_y = df_marks["Center Row"]
    
    img_all_watersh = np.copy(plt.imread(path_regions_watersh))
    img_all_mpp = np.copy(plt.imread(path_regions_mpp))
    
    img_all_watersh[img_all_watersh<3] = 0
    
    for n_ell in range(1,len(list_center_x)+1):
        n_list = n_ell-1
        center_x = list_center_x[n_list]
        center_y = list_center_y[n_list]
        
        val_center_water = img_all_watersh[center_x,center_y]
        val_center_mpp = img_all_mpp[center_x,center_y]
        
        img_all_watersh[img_all_watersh == val_center_water] = val_center_mpp
        
    io.imwrite("/home/jerome/Stage_Classif_Organoid/Img_marker_watershed_segmentation/Corresp_Ellipses.png", img_all_watersh)
        
    
    

def Separate_Ellipses(path_output):
    
    
    
    
    for n in range(3,45):
        img_ell = img_all[img_all==n]
        io.imwrite(path_output+"/local_map_{n}", img_ell)
    



path_output_t = "/home/jerome/Stage_Classif_Organoid/Img_marker_watershed_segmentation/local_map_GFP-01_w24-DAPI_TIF"
path_csv_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Exemple_type/GFP-01_w24-DAPI_TIF-marks-2020y03m06d14h55m39s760l.csv"
path_regions_mpp_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Exemple_type/GFP-01_w24-DAPI_TIF-region-2020y03m06d14h55m39s760l.png"
path_regions_watersh_t = "/home/jerome/Stage_Classif_Organoid/Img_marker_watershed_segmentation/Regions_sementation_Xavier.tif"

Correspondance_ellipses(path_regions_mpp_t,path_regions_watersh_t,path_csv_t)

