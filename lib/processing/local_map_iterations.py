#!/home/jerome/anaconda3/bin/python3

"""Written by Jérôme Emonet"""

#Importation des modules.
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")
from lib.objects.GroupObj import *
from lib.results.graph import *
from lib.processing.intensity_profiling import *
from lib.results.param_calcul import *
from lib.processing.classif import classif
from lib.results.output_image import *
from lib.results.statistics import *
from decimal import Decimal


def local_map_iterations(img,path_output,path_csv,path_image,k):
    #Création du répertoire parent de stockage des résultats.
    output_path_analyze = f"{path_output}/Local_Map_Analyze"
    Path(output_path_analyze).mkdir(parents=True, exist_ok=True)
    
    #Ouverture des fichiers de sorties.
    file_info = open(f"{output_path_analyze}/Informations.txt","w")
    file_results = open(f"{output_path_analyze}/Resultats.txt","w")
    
    #Initialisation
    fig_all, ax_all = initialize_glob_graph()
    compact = GroupObjImage()
    cystic = GroupObjImage()
    waste = GroupObjImage()
    i_obj = 1
    
    while i_obj <= img.n_object:
        print("Ellipse numéro", i_obj, "en cours de traitement.")
        obj = img.list_object[i_obj-1]
        obj.create_window(img,img.list_distmap[i_obj-1])
        list_levels = level_list_creation(img,i_obj,k)
        list_sum, list_count = count_and_sum_level(obj,list_levels,k)
        obj.list_mean, k = mean_intensity_level(list_sum,list_count,k)
        
        ratio = 1/k
        x = list(frange(Decimal(ratio),Decimal(1+ratio),ratio))
        
        obj.threshold, diff_thresh = thresholding(obj.list_mean,k)
        obj.mean_0_50 = middle_part_obj(obj.list_mean,x)

        obj.taille = sum(list_count)
        obj.contour = make_contour(img.list_distmap[i_obj-1])
        obj.max_intensity = max(obj.list_mean)
        obj.max_indice = x[obj.list_mean.index(obj.max_intensity)]
        obj.mean_intensity = np.mean(obj.list_mean)
        obj.rapp_max_creux = obj.max_intensity/obj.mean_0_50
        
        obj, compact, cystic, waste = classif(obj, compact, cystic, waste)
        
        new_unitary_graph(i_obj, obj, x, output_path_analyze)
        plt.plot(x,obj.list_mean)
        
        save_images(obj,i_obj, output_path_analyze)
        write_informations(obj,i_obj,k,file_info,list_levels,list_sum,list_count)
        write_results(obj,i_obj,file_results,diff_thresh)
        
        i_obj += 1
    
    #Sauvegarde du graphique contenant les courbes de toutes les ellipses.
    fig_all.savefig(f"{output_path_analyze}/Graphic_all_{obj.type}s.png")
    plt.close()
    
    #Fermeture des fichiers
    file_results.close()
    file_info.close()
    
    dict_mean, dict_std = make_mean_std(compact, cystic, waste)
    excel_writing(dict_mean,dict_std, compact, cystic, waste, path_output)
    
    return compact,cystic,waste
