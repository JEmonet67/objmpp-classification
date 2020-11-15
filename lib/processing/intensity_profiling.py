import numpy as np
from decimal import Decimal

def level_list_creation(img,i_obj,k):
    max_x = np.max(img.list_distmap[i_obj-1])
    list_niveau = [0]
    i_Niveau = 1
    while len(list_niveau) <= k:
        Niveau = round(max_x/k*i_Niveau,5)
        list_niveau += [Niveau]
        i_Niveau+=1
    return list_niveau


def count_and_sum_level(obj,list_niveau,k):
    list_sum = [0] * k
    list_count = [0] * k
    for i in range(0,obj.local_distmap.shape[0]):
        for j in range(0,obj.local_distmap.shape[1]):
            value_distmap = round(obj.local_distmap[i,j],5)
            if value_distmap > 0:
                i_discretisation = 0
                Found = False
                while i_discretisation < len(list_niveau)-1 and Found == False:
                    if (value_distmap > list_niveau[i_discretisation] 
                    and value_distmap <= list_niveau[i_discretisation+1]):
                        list_count[i_discretisation] += 1
                        list_sum[i_discretisation] += obj.local_img[i,j]
                        Found = True
                    i_discretisation += 1
    return list_sum, list_count


def frange(start, stop, step):
    while start < stop:
        yield float(start)
        start += Decimal(step)
        
def cuting_curves(list_mean):
    borne_80 = int(round(len(list_mean)*0.8))
    liste_80_100 = list_mean[borne_80:]
    max_local = max(liste_80_100)
    borne_sup = list_mean.index(max_local)
    
    return list_mean[:borne_sup]