import numpy as np
import pandas as pd

def make_mean_std(compact, cystic, waste):
    dict_mean = {}
    dict_std = {}
    for key,value in compact.__dict__.items():
            dict_mean[key] = [np.mean(getattr(compact,key)).round(3),np.mean(getattr(cystic,key)).round(3),np.mean(getattr(waste,key)).round(3)]
            dict_std[key] = [np.std(getattr(compact,key)).round(3),np.std(getattr(cystic,key)).round(3),np.std(getattr(waste,key)).round(3)]
    
    return dict_mean, dict_std


def excel_writing(dict_mean,dict_std, compact, cystic, waste, path_output):
    sum_number = [np.sum(compact.number),np.sum(cystic.number),np.sum(waste.number)]
    list_result = [sum_number, dict_mean["number"], dict_std["number"],[compact.number, cystic.number, waste.number],
                    dict_mean["tailles"],dict_std["tailles"], [compact.tailles,cystic.tailles, waste.tailles], 
                    dict_mean["contours"],dict_std["contours"],[compact.contours,cystic.contours, waste.contours],
                    dict_mean["max_intensities"],dict_std["max_intensities"], [compact.max_intensities,cystic.max_intensities, waste.max_intensities],
                    dict_mean["max_indices"], dict_std["max_indices"], [compact.max_indices,cystic.max_indices, waste.max_indices],
                    dict_mean["mean_intensities"],dict_std["mean_intensities"], [compact.mean_intensities,cystic.mean_intensities, waste.mean_intensities],
                    dict_mean["means_creux"], dict_std["means_creux"], [compact.means_creux,cystic.means_creux, waste.means_creux],
                    dict_mean["rapps_max_creux"],dict_std["rapps_max_creux"],[compact.rapps_max_creux,cystic.rapps_max_creux, waste.rapps_max_creux],
                    dict_mean["thresholds"], dict_std["thresholds"],[compact.thresholds,cystic.thresholds, waste.thresholds]]

    col = ["Compact","Cystique","Déchet"]
    
    ind_niv1 = ["Nombre d'organoïdes","","","",
                "Taille","","",
                "Périmètre","","",
                "Maximum du profil","","",
                "Indice du maximum du profil","","",
                "Moyenne du profil","","",
                "Moyenne creux","","",
                "Rapport max/creux","","",
                "Seuil","",""]
    ind_niv2 = ["Total","Moyenne", "Ecart-type", "Liste", "Moyenne", "Ecart-type",  "Liste", "Moyenne", "Ecart-type",  "Liste", "Moyenne", "Ecart-type", 
                 "Liste", "Moyenne", "Ecart-type", "Liste", "Moyenne", "Ecart-type",  "Liste", "Moyenne", "Ecart-type",
                 "Liste", "Moyenne", "Ecart-type",  "Liste", "Moyenne", "Ecart-type", "Liste"]
    list_ind = [(niv1,niv2) for niv1,niv2 in zip(ind_niv1,ind_niv2)]
    ind = pd.MultiIndex.from_tuples(list_ind, names=["Paramètre","Statistique"])
    
    df_result = pd.DataFrame(list_result, columns = col, index = ind)
    df_result.to_csv(f"{path_output}/Stats_Paramètres_organoïdes.csv",index=True)