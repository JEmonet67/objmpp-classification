#!/home/jerome/anaconda3/bin/python3

#Importation des modules.
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")
import pandas as pd
import imageio as io
from skimage import img_as_ubyte
from decimal import Decimal

def intensity_profiling(path_file,path_csv,path_image,path_glob_ells,k):
    print("Début de l'algorithme.")
    
    #Création du répertoire parent de stockage des résultats.
    output_path_analyze = f"{path_file}/Local_Map_Analyze"
    Path(output_path_analyze).mkdir(parents=True, exist_ok=True)
    
    #Importation des coordonnées des ellipses depuis le fichier csv.
    df_marks = pd.read_csv(path_csv)
    list_center_x = df_marks["Center Col"]
    list_center_y = df_marks["Center Row"]
    list_maj_axis = df_marks["Semi Major Axis"]
    
    #Ouverture des fichiers.
    file_info = open(f"{output_path_analyze}/Informations.txt","w")
    file_resultats = open(f"{output_path_analyze}/Resultats.txt","w")
    
    img_global = plt.imread(path_image)
    img_glob_ells = plt.imread(path_glob_ells)
    
    #Création de la liste des niveaux.
    list_Niveau = [0]
    i_Niveau = 1
    while len(list_Niveau) <= k+1:
        Niveau = round(1/k*i_Niveau,5)
        list_Niveau += [Niveau]
        # if Niveau < 1:
        #     list_Niveau += [Niveau] + [Niveau + 1]
        # else:
        #     list_Niveau += [Niveau]
        i_Niveau+=1
    
    file_info.write(f"""\t Nombre de niveaux discrétisés : {len(list_Niveau)} \n"""
        + f"""Liste des niveau discrétisés : \n {list_Niveau} \n \n""")
    
    #Création de la figure ellipse all.
    fig_all = plt.figure()
    ax_all = plt.axes()
    plt.title(label="Intensité moyenne en fonction de la distance de toutes les ellipses")
    ax_all = ax_all.set(xlabel = "Distance au centre (%)",
                ylabel = "Intensité moyenne des pixels")
    
    #Initialisation.
    n = len(list_center_x)
    n_img = 1
    
    #EXEMPLE Calcul de la moyenne des seuils cystiques/compacts
    n_compact = 0
    n_cystique = 0
    sum_seuil_compact = 0
    sum_seuil_cystique = 0
    
    #Début des itérations sur les images.
    while n_img <= n:
        print("Ellipse numéro", n_img, "en cours de traitement.")
        #img_ellipse = plt.imread(f"{path_file}/local_map_{n_img}.png")
        img_ellipse = np.load(f"{path_file}/local_map_{n_img}.npy")

        #Mise en place des coordonnées.
        center_x = list_center_x[n_img-1]
        center_y = list_center_y[n_img-1]
        maj_axis = int(round(list_maj_axis[n_img-1]))

        bord_gauche = (center_x-maj_axis)
        bord_droit = (center_x+maj_axis) 
        bord_haut = (center_y-maj_axis)
        bord_bas = (center_y+maj_axis)
        
        if bord_gauche < 0:
            bord_gauche = 0
        if bord_haut < 0:
            bord_haut = 0
        if bord_droit > img_ellipse.shape[0]-1:
            bord_droit = img_ellipse.shape[0]-1
        if bord_bas > img_ellipse.shape[1]-1:
            bord_bas = img_ellipse.shape[1]-1
        
        coordonnees = [bord_gauche,bord_droit,bord_haut,bord_bas]
        
        
        #Création et sauvegarde des images locales de la carte des distances et de l'image d'origine.
        img_ell_locale = img_ellipse[coordonnees[2]:coordonnees[3],
                                     coordonnees[0]:coordonnees[1]]
        img_glob_locale = img_global[coordonnees[2]:coordonnees[3],
                                     coordonnees[0]:coordonnees[1]]
        img_glob_ells_locale = img_glob_ells[coordonnees[2]:coordonnees[3],
                                     coordonnees[0]:coordonnees[1]]
        
        # plt.imshow(img_ell_locale)
        # plt.show()
        if n_img in [4,5,7,8,19,12,14]:
            io.imwrite(f"{path_file}/Local_Map_Analyze/Compact_Image_locale_{n_img}.png",(img_ell_locale*255).astype(np.uint8))
            io.imwrite(f"{path_file}/Local_Map_Analyze/Compact_Global_Image_locale_{n_img}.png",img_as_ubyte(img_glob_ells_locale))
        else:
            io.imwrite(f"{path_file}/Local_Map_Analyze/Cystique_Image_locale_{n_img}.png",(img_ell_locale*255).astype(np.uint8))
            io.imwrite(f"{path_file}/Local_Map_Analyze/Cystique_Global_Image_locale_{n_img}.png",img_as_ubyte(img_glob_ells_locale))
        
        # io.imwrite(f"{path_file}/Local_Map_Analyze/Image_locale_{n_img}.png",(img_ell_locale*255).astype(np.uint8))
        # io.imwrite(f"{path_file}/Local_Map_Analyze/Global_Image_locale_{n_img}.png",img_as_ubyte(img_glob_ells_locale))
        
        #Début du parcours de l'ellipse en cours.
        list_somme = [0] * k
        list_count = [0] * k
        for i in range(0,img_ell_locale.shape[0]):
            for j in range(0,img_ell_locale.shape[1]):
                value_distmap = round(img_ell_locale[i,j],5)
                if value_distmap <= 1.0:
                    i_discretisation = 0
                    Found = False
                    while i_discretisation <= len(list_Niveau) and Found == False:
                        if (value_distmap >= list_Niveau[i_discretisation] 
                        and value_distmap <= list_Niveau[i_discretisation+1]):
                            list_count[i_discretisation] += 1
                            list_somme[i_discretisation] += img_glob_locale[i,j]
                            Found = True
                        i_discretisation += 1
        
        #Calcul de la liste des moyennes de l'ellipse en cours.
        i_mean = 0
        list_mean = []
        while i_mean < k:
            try:
                list_mean += [round(list_somme[i_mean]/list_count[i_mean],2)]
                i_mean += 1
            except ZeroDivisionError:
                i_mean += 1
        
        #Coupage des courbes entre 80 et 100.
        list_mean_cut = Coupage_courbes(list_mean)
        k_cut = len(list_mean_cut)
        ratio_cut = 1/k_cut
        
        #Création du seuil d'égalité entre l'intégrale des courbes avant/après.
        mean_seuil, seuil, diff_seuil = Seuillage(list_mean_cut,ratio_cut)
        
        #EXEMPLE Calcul des sommes des seuils cystiques/compacts
        if n_img in [4,5,7,8,19,12,14]:
            sum_seuil_compact += seuil
            n_compact += 1
        else:
            sum_seuil_cystique += seuil
            n_cystique += 1
        
        #Ecriture des coordonnées dans le fichier Information.txt.
        file_info.write(f"""Ellipse numéro {n_img} : Center ({center_x}, {center_y})  Major Axis ({maj_axis}) \n"""
        + f"""\t Coord box x = {coordonnees[0]} et {coordonnees[1]}. \n"""
        + f"""\t Coord box y = {coordonnees[2]} et {coordonnees[3]}. \n"""
        + f"""\t Nombre de moyennes calculées : {len(list_mean)}"""
        + f"""\t Nombre de niveau discrétisé final : {k_cut} \n \n""")

        #Ecriture des résultats de l'ellipse en cours.
        file_resultats.write(f"\t ---------   Ellipse numéro {n_img} --------- \n \n" + 
                                f"""\t Liste des sommes des intensités par niveau  : {len(list_somme)} éléments. 
                                \n {list_somme} \n \n""" +
                                f"""\t Liste des nombre de pixels par niveau : {len(list_count)} éléments. 
                                \n {list_count} \n \n""" +
                                f"""\t Liste des moyennes d'intensité par niveau : {len(list_mean)} éléments. 
                                \n {list_mean} \n \n""" +
                                f"""\t Liste des moyennes d'intensités coupées : {len(list_mean_cut)} éléments. 
                                \n {list_mean_cut} \n \n""" + 
                                f"""\t Seuil = {seuil} \n \t Moyenne au seuil = {mean_seuil} \n \t Différence au seuil = {diff_seuil} \n \n \n""")

        
        #Création du graphique de l'ellipse en cours.
        x = list(frange(Decimal(ratio_cut),Decimal(1+ratio_cut),ratio_cut))
        #x = list(frange(0,1,ratio_cut))
        
        #Bloc if permettant de pallier au fait que parfois une valeur très proche de 100 en trop
        #au lieu d'égal à 100 à cause de l'imprécision est ajoutée à  x.
        if len(x) > len(list_mean_cut):
            x = x[:-1]
        fig_ell = plt.figure()
        ax_ell = plt.axes()
        plt.title(f"""Intensité moyenne en fonction de la
                  distance dans l'ellipse {n_img}""")
        ax_ell = ax_ell.set(xlabel = "Distance au centre (%)",
                    ylabel = "Intensité moyenne des pixels")

        plt.plot(x, list_mean_cut)
        plt.vlines(seuil,0,200,
                   colors="r",linestyles="dashed")
        #Bloc de code uniquement pour le test des exemples déjà classifiés.
        if n_img in [4,5,7,8,19,12,14]:
            fig_ell.savefig(f"{output_path_analyze}/Compact_graphic_ellipse_{n_img}.png")
        else:
            fig_ell.savefig(f"{output_path_analyze}/Cystique_graphic_ellipse_{n_img}.png")
        plt.close()
        
        #Ajout de la courbe de l'ellipse en cours dans le graphique contenant toutes les ellipses.
        plt.plot(x, list_mean_cut)
        #plt.plot(x, list_mean)

        
        n_img+=1
    
    
    #Sauvegarde du graphique contenant les courbes de toutes les ellipses.
    fig_all.savefig(f"{output_path_analyze}/graphic_ellipse_all.png")
    
    #Fermeture des fichiers
    file_resultats.close()
    file_info.close()
    
    
    #EXEMPLE Calcul de la moyenne des seuils cystiques/compacts
    mean_seuil_compact = sum_seuil_compact/n_compact
    mean_seuil_cystique = sum_seuil_cystique/n_cystique
    
    with open(f"{output_path_analyze}/Resultats.txt","r+") as f:
        content = f.read()
        f.seek(0,0)
        line = (f"""Moyenne seuil compact = {mean_seuil_compact}""" +
        f"""\t Moyenne seuil cystique = {mean_seuil_cystique}""")
        f.write(line.rstrip("\r\n") + "\n \n" + content)
    
    

    
    
    
    


def Coupage_courbes(list_mean):
    borne_80 = int(round(len(list_mean)*0.8))
    liste_80_100 = list_mean[borne_80:]
    max_local = max(liste_80_100)
    borne_sup = list_mean.index(max_local)
    
    return list_mean[:borne_sup]


def Seuillage(list_mean_cut,ratio_cut):
    list_diff = []
    list_seuil = list(frange(Decimal(ratio_cut), Decimal(100+ratio_cut), ratio_cut))

    for i_seuil in range(1,len(list_mean_cut)+1):
        sup_seuil = list_mean_cut[i_seuil:]
        inf_seuil = list_mean_cut[:i_seuil]
        diff_integral = round((sum(sup_seuil)-sum(inf_seuil)),5)
        list_diff += [diff_integral]
    
    min_diff = abs(list_diff[0])
    
    for diff in list_diff[1:]:
        if abs(diff) < min_diff:
            min_diff = diff
    
    Index_min = list_diff.index(min_diff)
    
    return list_mean_cut[Index_min], list_seuil[Index_min], list_diff[Index_min]
        
        
def frange(start, stop, step):
    while start < stop:
        yield float(start)
        start += Decimal(step)


#Attributions des 4 variables nécessaires à la fonction (test).
path_file_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Test/Test_organoïde_trié_V2"
path_csv_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Test/Test_organoïde_trié_marks_V2.csv"
path_image_t = "/home/jerome/Stage_Classif_Organoid/Image_Organoïdes/Images_transformées/GFP-01_w24-DAPI.tif"
path_glob_ells_t = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Test/GFP-01_w24-DAPI_TIF-ellipse-2020y03m11d15h42m57s248l.png"
k_t = 20

#Lancement de la fonction (test).
intensity_profiling(path_file_t,path_csv_t,path_image_t,path_glob_ells_t,k_t)
