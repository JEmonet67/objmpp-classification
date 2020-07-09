"""Written by Jérôme Emonet"""

from objmpp_classification.main.seg_orga_watershed import *
from objmpp_classification.main.classification_organoides import *
from objmpp_classification.main.traitements_objet import *
import pickle
import re


def organoid_classification(path_data, path_images, dilation=False, debug=False):
	"""Run Organoid classification from obj.MPP output"""
	print("Début du programme")
	#Initialisation.
	list_folder = [f for f in listdir(path_data) if "" == splitext(f)[1]]
	regexp_id = re.compile(r'[0-9]{4}y([0-9]{2}[mdhs]){5}[0-9]{3}l')
	regexp_name = re.compile(r'(.*_.*)_(.*)')
	all_number = [0,0,0]
	all_compact = {}
	all_cystique = {}
	all_dechet = {}
 
	#Itérations sur chaque dossier/image.
	for objmpp_folder in list_folder:
		print("Fichier image en cours :",objmpp_folder)
		path_img_folder = path_data+"/"+objmpp_folder
		list_ref = [splitext(ref_img)[0] for ref_img in listdir(path_img_folder) if ".csv" == splitext(ref_img)[1]]
		for ref in list_ref:
			print("Initialisation des chemins...")
			#Récupération du nom et de l'id de l'image en cours.
			id_image = regexp_id.search(ref).group(0)
			name_img = ref.replace(f"-marks-{id_image}","")
			name_img = re.sub(regexp_name,r'\1.\2',name_img)

			#Récupération des chemins requis pour la suite.
			#Vérification des fichiers.
			#Ajouter des blocs if/raise pour chaque élément afin de vérifier qu'ils existent et sinon envoyer une erreur explicite.
			list_files_id = [files for files in listdir(path_img_folder) if id_image in files]
			for files_id in list_files_id:
				if "region" in files_id:
					path_region = path_img_folder + "/" + files_id
				elif "marks" in files_id:
					path_csv = path_img_folder + "/" + files_id
			path_img = path_images + "/" + name_img
   
			print("Mise en place des composantes du Watershed.")
			#Création des régions binarisées et érodées.
			img_all_regions = cv.imread(path_region,0)
			all_ell_sep = Separate_ellipses(img_all_regions)
			list_ells_mapdist = Distance_map(all_ell_sep)
			all_ell_erod = Erode_ellipses(list_ells_mapdist)
			if dilation != False:
				all_ell = Dilate_ellipses(all_ell_sep)
			else:
				all_ell = Binaryze_ellipses(path_region)
			
			print("Watershed en cours...")
			#Segmentation Watershed.
			Path(path_img_folder+"/Watershed").mkdir(parents=True, exist_ok=True)
			watershed = Seq_Water_meth2(path_img,all_ell,all_ell_erod,path_img_folder+"/Watershed",10)

			print("Séparation des objets issu du watershed.")
			#Séparation des objets watershed.
			Path(path_img_folder+"/local_map_watershed").mkdir(parents=True, exist_ok=True)
			list_regions_obj = Separate_ells_watershed(watershed,path_csv)
			file_list_regions_obj = open(path_img_folder+"/local_map_watershed/Liste_regions_objets.txt","wb")
			pickle.Pickler(file_list_regions_obj).dump(list_regions_obj)
			file_list_regions_obj.close()
   
			print("Transformation des objets en map des distance.")
			#Transformation des objets en map des distance.
			list_dm_obj = Distance_map(list_regions_obj, path_img_folder+"/local_map_watershed")
			file_list_dm_obj = open(path_img_folder+"/local_map_watershed/Liste_dist_map_objets.txt","wb")
			pickle.Pickler(file_list_dm_obj).dump(list_dm_obj)
			file_list_dm_obj.close()
			
			print("Début de l'algorithme de classification.")
			#Classification des organoïdes.
			number,compact,cystique,dechet = intensity_profiling(list_dm_obj,path_img_folder,path_csv,path_img,20)
			
			print("Ajout des statistiques des organoides à la liste totale.")
			#Somme global de toutes les images.
			all_number = add_list(number, all_number)
			all_compact = add_dico(compact,all_compact)
			all_cystique = add_dico(cystique,all_cystique)
			all_dechet = add_dico(dechet,all_dechet)

	print("Mise en place de l'excel des statistiques global.")
	#Calcul des statistiques globales.
	dict_mean, dict_std = statistiques(all_compact,all_cystique,all_dechet)

	#Mise en place du excel global.
	excel_writing(dict_mean, dict_std, all_number, path_data)
   
def add_list(list1, list2):
	i=0
	for elt in list1:
		list2[i] += elt
		i += 1
	
	return list2
    
def add_dico(dico1, dico2):
	for elt in dico1:
		if elt not in dico2:
			dico2[elt] = dico1[elt]
		else:
			dico2[elt] += dico1[elt]
	
	return dico2
			
			
	    
path_data = "/home/jerome/Stage_Classif_Organoid/Result_MPP/Organoïd/images-organoides-GFP_dilated"
path_images = "/home/jerome/Stage_Classif_Organoid/Image_Organoïdes/07012020-UBTD1-video"
organoid_classification(path_data,path_images,dilation=True)

	    
