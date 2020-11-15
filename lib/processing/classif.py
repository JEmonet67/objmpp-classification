
def classif(obj, compact, cystic, waste):

    if obj.max_indice >= 0.85 and obj.threshold >= 0.55 and obj.rapp_max_creux>=1.45:
        obj.subtype = "cystic"
        cystic.number += 1
        cystic.tailles += [obj.taille]
        cystic.contours += [obj.contour]
        cystic.max_intensities += [obj.max_intensity]
        cystic.max_indices += [obj.max_indice]
        cystic.mean_intensities += [obj.mean_intensity]
        cystic.rapps_max_creux += [obj.rapp_max_creux]
        cystic.means_creux += [obj.mean_0_50]
        cystic.thresholds += [obj.threshold]
        
    elif obj.mean_intensity >=75:
        obj.subtype = "compact"
        compact.number += 1
        compact.tailles += [obj.taille]
        compact.contours += [obj.contour]
        compact.max_intensities += [obj.max_intensity]
        compact.max_indices += [obj.max_indice]
        compact.mean_intensities += [obj.mean_intensity]
        compact.rapps_max_creux += [obj.rapp_max_creux]
        compact.means_creux += [obj.mean_0_50]
        compact.thresholds += [obj.threshold]
        
    else:
        obj.subtype = "waste"
        waste.number += 1
        waste.tailles += [obj.taille]
        waste.contours += [obj.contour]
        waste.max_intensities += [obj.max_intensity]
        waste.max_indices += [obj.max_indice]
        waste.mean_intensities += [obj.mean_intensity]
        waste.rapps_max_creux += [obj.rapp_max_creux]
        waste.means_creux += [obj.mean_0_50]
        waste.thresholds += [obj.threshold]
        
    return obj, compact, cystic, waste
        
