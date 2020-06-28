#!/home/jerome/anaconda3/bin/python3

#Importation des modules.
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import imageio as io
from skimage import img_as_ubyte
import pandas as pd


    
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
    


path_output_t = "/home/jerome/Stage_Classif_Organoid/Img_marker_watershed_segmentation"
path_csv_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Exemple_type/GFP-01_w24-DAPI_TIF-marks-2020y03m06d14h55m39s760l.csv"
path_regions_t = "/home/jerome/Stage_Classif_Organoid/Img_marker_watershed_segmentation/Regions_sementation_Xavier.tif"

Separate_ellipses(path_output_t,path_regions_t,path_csv_t)

