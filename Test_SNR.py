import SNR
import bruit
import filtrage

from datetime import datetime
import skimage as sk
import matplotlib.pyplot as plt
import os
from colorama import Back, Fore, Style, deinit, init

####################################################################################
#   
# Test des fonctions de filtrage sur du bruit additif
#
####################################################################################

if __name__ == '__main__':
    
    init() # Initialisation de colorama
    chemin_image_reference = "./images_reference/image2_reference.png"
    image_reference = sk.io.imread(chemin_image_reference)

    # --- initialisation pour collecte des résultats 3D ---
    import numpy as np
    taille_noyau = [3, 5, 7]                        # correspond à rayon_noyau = 1,2,3
    niveau_bruit = ['faible', 'moyen', 'élevé']
    bruit_types = ['additif', 'multiplicatif', 'sel_poivre']

    methodes = [
        'median_crop', 'median_extension', 'median_miroir', 'median_wrap',
        'conv_rect_crop','conv_rect_ext','conv_rect_miroir','conv_rect_wrap',
        'conv_circ_crop','conv_circ_ext','conv_circ_miroir','conv_circ_wrap',
        'conv_pyr_crop','conv_pyr_ext','conv_pyr_miroir','conv_pyr_wrap',
        'conv_cone_crop','conv_cone_ext','conv_cone_miroir','conv_cone_wrap'
    ]

    # SNR_bruite[bruit] -> list des SNR bruités par niveau (len == 3)
    SNR_bruite = {b: [] for b in bruit_types}
    # SNR_debruite_final[bruit][method] -> list (len niveau_bruit) de listes (une par niveau) qui contiennent les SNR par taille de noyau
    SNR_debruite_final = {b: {m: [ [] for _ in niveau_bruit ] for m in methodes} for b in bruit_types}
    # --- fin initialisation ---
    
    #On teste 3 niveaux de bruit
    #1: faible
    #2: moyen
    #3: élevé
    for puissance_bruit in range(1,4):
        
        bruit_additif = 20
        bruit_multiplicatif = 0.2
        bruit_sel_et_poivre = (0.02,0.02)
        
        #On augmente l'intensité du bruit
        bruit_additif *= puissance_bruit**2
        bruit_multiplicatif *= puissance_bruit**2
        bruit_sel_et_poivre = (bruit_sel_et_poivre[0]*puissance_bruit**2,bruit_sel_et_poivre[1]*puissance_bruit**2)
        
        #A l'aide de l'image de référence, on génère une image bruitée
        #On l'a met dans une varaible & on la sauvegarde
        image_bruitee_additif = bruit.bruit_additif(chemin_image_reference, bruit_additif)
        sk.io.imsave("./images_reference/image_bruitee_test_additif.png", image_bruitee_additif)
        #On calcule le SNR entre l'image de référence et l'image bruitée
        SNR_bruité_additif = SNR.calcul_SNR(image_reference, image_bruitee_additif)
        
        #A l'aide de l'image de référence, on génère une image bruitée
        #On l'a met dans une varaible & on la sauvegarde
        image_bruitee_multiplicatif = bruit.bruit_multiplicatif(chemin_image_reference, bruit_multiplicatif)
        sk.io.imsave("./images_reference/image_bruitee_test_multiplicatif.png", image_bruitee_multiplicatif)
        #On calcule le SNR entre l'image de référence et l'image bruitée
        SNR_bruité_multiplicatif = SNR.calcul_SNR(image_reference, image_bruitee_multiplicatif)
        
        #A l'aide de l'image de référence, on génère une image bruitée 
        #On l'a met dans une varaible & on la sauvegarde
        image_bruitee_s_p = bruit.bruit_salt_and_pepper(chemin_image_reference,bruit_sel_et_poivre[0],bruit_sel_et_poivre[1])
        sk.io.imsave("./images_reference/image_bruitee_test_salt_pepper.png", image_bruitee_s_p)
        #On calcule le SNR entre l'image de référence et l'image bruitée
        SNR_bruité_s_p = SNR.calcul_SNR(image_reference, image_bruitee_s_p)
        
        # noise_idx = puissance_bruit - 1
        SNR_bruite['additif'].append(SNR_bruité_additif)
        SNR_bruite['multiplicatif'].append(SNR_bruité_multiplicatif)
        SNR_bruite['sel_poivre'].append(SNR_bruité_s_p)
        
        print(Fore.RED + "\n\n=== Niveau de bruit : ",["faible","moyen","élevé"][puissance_bruit-1]," ===")
        for puissance_rayon in range(1,4):
    
            rayon_noyau = 1
            #On augmente la taille du noyau
            rayon_noyau *= puissance_rayon
            
            resultat_median=[]
            resultat_convolution=[]

            print(Fore.MAGENTA + "\n\n=== Taille de la matrice filtre : ",["3x3","5x5","7x7"][puissance_rayon-1]," pixels === \n")

            print(Fore.YELLOW + "=== Test des fonctions de filtrage sur du bruit additif ==="+Style.RESET_ALL)
            
            print("=== SNR de l'image bruitée : ", SNR_bruité_additif)
            
            #On fait des tests avec les différentes méthodes de filtrage
            
            #On test Crop
            #On teste median
            image_debruitee = filtrage.filtrage_median_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['additif']['median_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (median crop) : ", SNR_debruite)
            
            #On test extension
            #On test median
            image_debruitee = filtrage.filtrage_median_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['additif']['median_extension'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (median extension) : ", SNR_debruite)
            
            #On test miroir
            #On test median
            image_debruitee = filtrage.filtrage_median_miroir("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['additif']['median_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruite)
            
            #On test wrap
            #On test median
            image_debruitee = filtrage.filtrage_median_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['additif']['median_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruite)
            
            #On test convolution crop rectangular
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_rect_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution rectangular crop) : ", SNR_debruite)
            
            #On test convolution extension rectangular
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_rect_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution rectangular extension) : ", SNR_debruite)
            
            #On test convolution miroir rectangular
            image_debruitee = filtrage.filtrage_convolution_miroir("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_rect_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution rectangular miroir) : ", SNR_debruite)
            
            #On test convolution wrap rectangular
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_rect_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution rectangular wrap) : ", SNR_debruite)
            
            #On teste les filtres de convolution  
            #On test le filtre circular
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_circ_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution circular crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_circ_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution circular extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_circ_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution circular miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_circ_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution circular wrap) : ", SNR_debruite)
            
            #Pyramidal crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_pyr_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution pyramidal crop) : ", SNR_debruite)
            
            #Pyramidal extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_pyr_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution pyramidal extension) : ", SNR_debruite)
            
            #Pyramidal miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_pyr_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution pyramidal miroir) : ", SNR_debruite)
            
            #Pyramidal wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_pyr_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution pyramidal wrap) : ", SNR_debruite)
            
            #Cone crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_cone_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution cone crop) : ", SNR_debruite)
            
            #Cone extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_cone_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution cone extension) : ", SNR_debruite)
            
            #Cone miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_cone_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution cone miroir) : ", SNR_debruite)
            
            #Cone wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['additif']['conv_cone_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_additif)
            print("=== SNR de l'image débruitée (convolution cone wrap) : ", SNR_debruite)

            print(Fore.GREEN +"\n=== Le meilleur résultat de SNR pour ce bruit avec un niveau de bruit additif de ",bruit_additif," et un rayon de ",rayon_noyau," pixels est : ")
            #On veut récupérer le max et l'indice pour afficher la méthode d'extension la meilleure
            max_median = max(resultat_median)
            indice_median = resultat_median.index(max_median)
            max_convolution = max(resultat_convolution)
            indice_convolution = resultat_convolution.index(max_convolution)
            if max_median > max_convolution :
                print("Median avec la méthode :",["Crop","Extension","Miroir","Wrap"][indice_median],"avec un SNR de :",max_median)
            else :
                print("Convolution avec la méthode :",["Crop rectangular","Extension rectangular","Miroir rectangular","Wrap rectangular",
                                                      "Crop circular","Extension circular","Miroir circular","Wrap circular",
                                                      "Crop pyramidal","Extension pyramidal","Miroir pyramidal","Wrap pyramidal",
                                                      "Crop cone","Extension cone","Miroir cone","Wrap cone"
                                                      ][indice_convolution],"avec un SNR de :",max_convolution)
            resultat_median.clear()
            resultat_convolution.clear()

####################################################################################
#   
# Test des fonctions de filtrage sur du bruit multiplicatif
#
####################################################################################

            print("\n")
            print(Fore.YELLOW + "=== Test des fonctions de filtrage sur du bruit multiplicatif ===" + Style.RESET_ALL)
          
            print("=== SNR de l'image bruitée : ", SNR_bruité_multiplicatif)
            
            #On fait des tests avec les différentes méthodes de filtrage
            
            #On test Crop
            #On teste median
            image_debruitee = filtrage.filtrage_median_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['median_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (median crop) : ", SNR_debruite)
            
            #On test extension
            image_debruitee = filtrage.filtrage_median_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['median_extension'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (median extension) : ", SNR_debruite)
            
            #On test miroir
            image_debruitee = filtrage.filtrage_median_miroir("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['median_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruite)
            
            #On test wrap
            image_debruitee = filtrage.filtrage_median_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['median_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruite)
            
            #On test convolution crop rectangular
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_rect_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution rectangular crop) : ", SNR_debruite)
            
            #On test convolution extension rectangular
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_rect_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution rectangular extension) : ", SNR_debruite)
            
            #On test convolution miroir rectangular
            image_debruitee = filtrage.filtrage_convolution_miroir("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_rect_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution rectangular miroir) : ", SNR_debruite)
            
            #On test convolution wrap rectangular
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_rect_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution rectangular wrap) : ", SNR_debruite)
            
            # circular - crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_circ_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution circular crop) : ", SNR_debruite)

            # circular - extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_circ_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution circular extension) : ", SNR_debruite)

            # circular - miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_circ_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution circular miroir) : ", SNR_debruite)

            # circular - wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_circ_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution circular wrap) : ", SNR_debruite)

            # pyramidal - crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_pyr_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution pyramidal crop) : ", SNR_debruite)

            # pyramidal - extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_pyr_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution pyramidal extension) : ", SNR_debruite)

            # pyramidal - miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_pyr_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution pyramidal miroir) : ", SNR_debruite)

            # pyramidal - wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_pyr_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution pyramidal wrap) : ", SNR_debruite)

            # cone - crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_cone_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution cone crop) : ", SNR_debruite)

            # cone - extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_cone_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution cone extension) : ", SNR_debruite)

            # cone - miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_cone_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution cone miroir) : ", SNR_debruite)

            # cone - wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['multiplicatif']['conv_cone_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_multiplicatif)
            print("=== SNR de l'image débruitée (convolution cone wrap) : ", SNR_debruite)
                        
            print(Fore.GREEN + "\n=== Le meilleur résultat de SNR pour ce bruit avec un niveau de bruit multiplicatif de ",bruit_multiplicatif," et un rayon de ",rayon_noyau," pixels est : ")
            #On veut récupérer le max et l'indice pour afficher la méthode d'extension la meilleure
            max_median = max(resultat_median)
            indice_median = resultat_median.index(max_median)
            max_convolution = max(resultat_convolution)
            indice_convolution = resultat_convolution.index(max_convolution)
            if max_median > max_convolution :
                print("Median avec la méthode :",["Crop","Extension","Miroir","Wrap"][indice_median],"avec un SNR de :",max_median)
            else :
                print("Convolution avec la méthode :",["Crop rectangular","Extension rectangular","Miroir rectangular","Wrap rectangular",
                                                      "Crop circular","Extension circular","Miroir circular","Wrap circular",
                                                      "Crop pyramidal","Extension pyramidal","Miroir pyramidal","Wrap pyramidal",
                                                      "Crop cone","Extension cone","Miroir cone","Wrap cone"
                                                      ][indice_convolution],"avec un SNR de :",max_convolution)
            resultat_median.clear()
            resultat_convolution.clear()

####################################################################################
#   
# Test des fonctions de filtrage sur du bruit sel & poivre
#
####################################################################################

            print("\n")
            print(Fore.YELLOW + "=== Test des fonctions de filtrage sur du bruit sel & poivre ===" + Style.RESET_ALL)
            
            print("=== SNR de l'image bruitée : ", SNR_bruité_s_p)
            
            #On fait des tests avec les différentes méthodes de filtrage
            
            #On test Crop
            #On teste median
            image_debruitee = filtrage.filtrage_median_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['median_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (median crop) : ", SNR_debruite)
            
            #On test extension
            #On test median
            image_debruitee = filtrage.filtrage_median_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['median_extension'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (median extension) : ", SNR_debruite)
            
            #On test miroir
            #On test median
            image_debruitee = filtrage.filtrage_median_miroir("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['median_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruite)

            #On test wrap
            #On test median
            image_debruitee = filtrage.filtrage_median_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['median_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruite)
            
             #On test convolution rectangular crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_rect_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution rectangular crop) : ", SNR_debruite)
            
            #On test convolution rectangular extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_rect_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution rectangular extension) : ", SNR_debruite)
            
            #On test convolution miroir rectangular
            image_debruitee = filtrage.filtrage_convolution_miroir("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_rect_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution rectangular miroir) : ", SNR_debruite)
            
            #On test convolution wrap rectangular
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_rect_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution rectangular wrap) : ", SNR_debruite)

            #On test le filtre circular
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_circ_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution circular crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_circ_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution circular extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_circ_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution circular miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_circ_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution circular wrap) : ", SNR_debruite)
            
            #On test le filtre pyramidal
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_pyr_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution pyramidal crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_pyr_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution pyramidal extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_pyr_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution pyramidal miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_pyr_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution pyramidal wrap) : ", SNR_debruite)
            
            #Cone crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_cone_crop'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution cone crop) : ", SNR_debruite)
            
            #Cone extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_cone_ext'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution cone extension) : ", SNR_debruite)
            
            #Cone miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_cone_miroir'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution cone miroir) : ", SNR_debruite)
            
            #Cone wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            SNR_debruite_final['sel_poivre']['conv_cone_wrap'][puissance_bruit - 1].append(SNR_debruite - SNR_bruité_s_p)
            print("=== SNR de l'image débruitée (convolution cone wrap) : ", SNR_debruite)
                        
            print(Fore.GREEN +"\n=== Le meilleur résultat de SNR pour ce bruit avec un niveau de bruit sel & poivre de probabilité respective : ",bruit_sel_et_poivre[0], ", ", bruit_sel_et_poivre[1]," et un rayon de ",rayon_noyau," pixels est : ")
            #On veut récupérer le max et l'indice pour afficher la méthode d'extension la meilleure
            max_median = max(resultat_median)
            indice_median = resultat_median.index(max_median)
            max_convolution = max(resultat_convolution)
            indice_convolution = resultat_convolution.index(max_convolution)
            if max_median > max_convolution :
                print("Median avec la méthode :",["Crop","Extension","Miroir","Wrap"][indice_median],"avec un SNR de :",max_median)
            else :
                print("Convolution avec la méthode :",["Crop rectangular","Extension rectangular","Miroir rectangular","Wrap rectangular",
                                                      "Crop circular","Extension circular","Miroir circular","Wrap circular",
                                                      "Crop pyramidal","Extension pyramidal","Miroir pyramidal","Wrap pyramidal",
                                                      "Crop cone","Extension cone","Miroir cone","Wrap cone"
                                                      ][indice_convolution],"avec un SNR de :",max_convolution)

    # convertir en tableaux numpy (shape = (len(niveau_bruit), len(taille_noyau)))
    for b in bruit_types:
        SNR_bruite[b] = np.array(SNR_bruite[b])
        for m in methodes:
            # chaque SNR_debruite_final[b][m] est une liste de 3 listes (une par niveau), chacune contenant len(taille_noyau) valeurs
            SNR_debruite_final[b][m] = np.array([row for row in SNR_debruite_final[b][m]])
            
####################################################################################
#   
# Affichage des résultats
#
####################################################################################  

    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(15, 10), sharex=True)
    cmap = plt.get_cmap('tab20')
    colors = [cmap(i) for i in range(len(methodes))]

    for i, b in enumerate(bruit_types):
            for j, lvl in enumerate(niveau_bruit):
                    ax = axs[i, j]
                    
                    # Tracer chaque méthode
                    for idx, m in enumerate(methodes):
                        y = SNR_debruite_final[b][m][j]
                        ax.plot(taille_noyau, y, label=m,
                                color=colors[idx], linewidth=1,
                                marker='o', markersize=2)
                    
                    # Ajuste automatiquement l’échelle
                    ymin, ymax = ax.get_ylim()
                    ax.set_ylim(ymin, ymax)  # force matplotlib à recaler
                    ax.set_title(f"{b} — {lvl}")
                    
                    if j == 0:
                        ax.set_ylabel("Gain de SNR")
                    if i == 2:  # dernière ligne
                        ax.set_xlabel("Taille du noyau")
                    
                    ax.grid(True, linestyle=':', linewidth=0.4, alpha=0.5)

    # Légende globale (simple)
    fig.legend(methodes, loc='center right', bbox_to_anchor=(1.02, 0.5))
    fig.tight_layout(rect=[0, 0, 0.88, 1])

    path_graphe="./graphique/graphique_snr_3x3_"+str(datetime.now().strftime("%Hh%M_%d_%m_%Y"))+".png"
    plt.savefig(path_graphe, dpi=200)
    print("Image des graphes enregistrés dans :"+path_graphe)
    
    plt.close(fig)          

    #On supprime les images créées
    os.remove("./images_reference/image_bruitee_test_multiplicatif.png")
    os.remove("./images_reference/image_bruitee_test_salt_pepper.png")
    os.remove("./images_reference/image_bruitee_test_additif.png")
    
    deinit() # pour arrêter colorama
