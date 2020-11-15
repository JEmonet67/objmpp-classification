import cv2 as cv
import numpy as np
import imageio as io
import pickle

def save_images(obj,i_obj, path_output):
    img_locale_norm = cv.normalize(obj.local_img, np.zeros(obj.local_img.shape),0, 255, cv.NORM_MINMAX)
    distmap_locale_norm = cv.normalize(obj.local_distmap, np.zeros(obj.local_distmap.shape),0, 255, cv.NORM_MINMAX)
    #io.imwrite(f"{path_output}/{obj.type}_{obj.subtype}_{i_obj}_distancemap.png",(np.uint8(distmap_locale_norm)))
    io.imwrite(f"{path_output}/{obj.type}_{obj.subtype}_{i_obj}.png",np.uint8(img_locale_norm))

def write_informations(obj,i_obj,k,file_info,list_levels,list_sum,list_count):
    #Ecriture des niveaux discrétisés de chaque ellipse dans le fichier d'info.
    file_info.write(f"\t ---------   {obj.type} numéro {i_obj} {obj.subtype} --------- \n \n"
                    + f"""Liste des niveau discrétisés ellipse : {k} \n \n"""
                    + f"""Liste des bornes des intervalles de niveau ({len(list_levels)}) : \n {list_levels} \n \n""")
    
    #Ecriture des coordonnées dans le fichier Information.txt.
    file_info.write(f"""\t Center ({obj.center.x}, {obj.center.y})  Major Axis ({obj.major_axis}) \n"""
                    + f"""\t Coord box x = {obj.coordinates[0]} et {obj.coordinates[1]}. \n"""
                    + f"""\t Coord box y = {obj.coordinates[2]} et {obj.coordinates[3]}. \n \n""")
    
    #Ecriture des caractéristiques des profils de niveaux dans le fichier d'info.
    file_info.write(f"""Liste des sommes des intensités par niveau  : {len(list_sum)} éléments. 
                    \n {list_sum} \n \n"""
                    + f"""Liste des nombre de pixels par niveau : {len(list_count)} éléments. 
                    \n {list_count} \n \n"""
                    + f"""Liste des moyennes d'intensité par niveau : {len(obj.list_mean)} éléments. 
                    \n {obj.list_mean} \n \n \n""")
    
    
def write_results(obj,i_obj,file_results, diff_thresh):
    #Ecriture des résultats de l'ellipse en cours.
    file_results.write(f"\t ---------   {obj.type} numéro {i_obj} {obj.subtype} --------- \n \n"
                        + f""" Taille de l'ellipse (nb de pixels) : {obj.taille} \n"""
                        + f""" Longueur du périmètre de l'ellipse : {obj.contour} \n"""
                        + f""" Maximum du profil d'intensité de l'ellipse : {obj.max_intensity} \n"""
                        + f""" Indice du maximum du profil d'intensité de l'ellipse : {obj.max_indice} \n"""
                        + f""" Moyenne du profil d'intensité de l'ellipse : {round(obj.mean_intensity,3)} \n"""
                        + f""" Moyenne du creux de l'ellipse (0-50) : {round(obj.mean_0_50,3)} \n"""
                        + f""" Rapport max/creux : {obj.rapp_max_creux} \n \n"""
                        + f""" Seuil = {round(obj.threshold,3)} \t Différence au threshold = {round(diff_thresh,3)} \n \n""")
    
def save_obj(obj_to_save,path_file):
        file_to_save = open(path_file,"wb")
        pickle.Pickler(file_to_save).dump(obj_to_save)
        file_to_save.close()