"""Written by Jérôme Emonet"""

from objmpp_classification.segmentation.seg_orga_watershed import *
from objmpp_classification.processing.local_map_iterations import *
from objmpp_classification.segmentation.traitements_objet import *
from objmpp_classification.objects.ImgObjMpp import ImgObjMpp
from os import listdir
from os.path import splitext
from pathlib import Path
import pickle
import re
from skimage import img_as_ubyte

def main(path_data, path_images, debug=False):
	"""Run Organoid classification from obj.MPP output"""
	print("Début du programme")
	#Initialisation.
	list_folder = [f for f in listdir(path_data) if "" == splitext(f)[1]]
	regexp_id = re.compile(r'[0-9]{4}y([0-9]{2}[mdhs]){5}[0-9]{3}l')
	regexp_name = re.compile(r'(.*_.*)_(.*)')
	total_compact = GroupObjFile()
	total_cystic = GroupObjFile()
	total_waste = GroupObjFile()
	n_file = 0
 
	#Itérations sur chaque dossier/image.
	for objmpp_folder in list_folder:
		n_file += 1
		print("Progression : ",n_file,"/",len(list_folder), " ", len(list_folder)-n_file+1, "fichiers restants")
		print("Image en cours :",objmpp_folder)
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

			#Initialisation image.
			img = ImgObjMpp(path_img,path_region,path_csv)

			print("Mise en place des composantes du Watershed.")
			#Création des régions binarisées et érodées.
			ells_sep = Separate_ellipses(img.matrix_regions)
			distmap_sep = Distance_map(ells_sep)
			distmap_erod = Erode_ellipses(distmap_sep)
			binary_ells = Binaryze_ellipses(path_region)
			
			print("Watershed en cours...")
			#Segmentation Watershed.
			Path(path_img_folder+"/Watershed").mkdir(parents=True, exist_ok=True)
			watershed = Seq_Water_meth2(path_img,binary_ells,distmap_erod,path_img_folder+"/Watershed",10)

			print("Séparation des objets issu du watershed.")
			#Séparation des objets watershed.
			#Path(path_img_folder+"/local_map_watershed").mkdir(parents=True, exist_ok=True)
			img = Separate_ells_watershed(img,watershed,path_csv)
   
			print("Transformation des objets en map des distance.")
			#Transformation des objets en map des distance.
			img.list_distmap = Distance_map(img.list_reg_watersh)
			
			print("Début de l'algorithme de classification.")
			#Classification des organoïdes.
			compact,cystic,waste = local_map_iterations(img,path_img_folder,path_csv,path_img,20)
			
			# print("Ajout des statistiques des organoides à la liste totale.")
			#Somme global de toutes les images.
			#print(f"TAAAIIIILLLE APRES {compact.tailles}")
			total_compact.add_GroupObjImage(compact)
			total_cystic.add_GroupObjImage(cystic)
			total_waste.add_GroupObjImage(waste)
			#print(f"TAIIIILLLE AVANT {total_compact.tailles}")
   
			#Ecriture fichiers objets.
			Path(path_img_folder+"/Objects").mkdir(parents=True, exist_ok=True)
			save_obj(img,path_img_folder+"/Objects/img")
			save_obj(total_compact,path_img_folder+"/Objects/total_compact")
			save_obj(total_compact,path_img_folder+"/Objects/total_cystic")
			save_obj(total_compact,path_img_folder+"/Objects/total_waste")

	
	#Calcul des statistiques globales.
	dict_mean, dict_std = make_mean_std(total_compact,total_cystic,total_waste)
 
 	# #Mise en place du excel global.
	excel_writing(dict_mean, dict_std, total_compact, total_cystic, total_waste, path_data)


   

			
			
	    
# path_data_t = "/home/jerome/Bureau/New_GFP"
# path_images_t = "/mnt/Shared Data/Stage_Classif_Organoid/Image_Organoïdes/07012020-UBTD1-video"
# main(path_data_t,path_images_t)

	    
