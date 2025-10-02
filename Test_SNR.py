import SNR
import bruit
import filtrage

import skimage as sk
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
            print("=== SNR de l'image débruitée (median crop) : ", SNR_debruite)
            
            #On test extension
            #On test median
            image_debruitee = filtrage.filtrage_median_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median extension) : ", SNR_debruite)
            
            #On test miroir
            #On test median
            image_debruitee = filtrage.filtrage_median_miroir("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruite)
            
            #On test wrap
            #On test median
            image_debruitee = filtrage.filtrage_median_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruite)
            
            #On test convolution crop rectangular
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular crop) : ", SNR_debruite)
            
            #On test convolution extension rectangular
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular extension) : ", SNR_debruite)
            
            #On test convolution miroir rectangular
            image_debruitee = filtrage.filtrage_convolution_miroir("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular miroir) : ", SNR_debruite)
            
            #On test convolution wrap rectangular
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular wrap) : ", SNR_debruite)
            
            #On teste les filtres de convolution  
            #On test le filtre circular
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular wrap) : ", SNR_debruite)
            
            #On test le filtre pyramidal
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal wrap) : ", SNR_debruite)
            
            #On test le filtre cone
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_additif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
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
            print("=== SNR de l'image débruitée (median crop) : ", SNR_debruite)
            
            #On test extension
            #On test median
            image_debruitee = filtrage.filtrage_median_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median extension) : ", SNR_debruite)
            
            #On test miroir
            #On test median
            image_debruitee = filtrage.filtrage_median_miroir("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruite)
            
            #On test wrap
            #On test median
            image_debruitee = filtrage.filtrage_median_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruite)
            
            #On test convolution rectangular crop 
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular crop) : ", SNR_debruite)
            
            #On test convolution rectangular extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular extension) : ", SNR_debruite)
            
            
            #On test convolution rectangular miroir
            image_debruitee = filtrage.filtrage_convolution_miroir("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular miroir) : ", SNR_debruite)
           
            #On test convolution rectangular wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular wrap) : ", SNR_debruite)
            
            #On test le filtre circular
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular wrap) : ", SNR_debruite)
            
            #On test le filtre pyramidal
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal wrap) : ", SNR_debruite)
            
            #On test le filtre cone
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_multiplicatif.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
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
            print("=== SNR de l'image débruitée (median crop) : ", SNR_debruite)
            
            #On test extension
            #On test median
            image_debruitee = filtrage.filtrage_median_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median extension) : ", SNR_debruite)
            
            #On test miroir
            #On test median
            image_debruitee = filtrage.filtrage_median_miroir("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruite)

            #On test wrap
            #On test median
            image_debruitee = filtrage.filtrage_median_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_median.append(SNR_debruite)
            print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruite)
            
             #On test convolution rectangular crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular crop) : ", SNR_debruite)
            
            #On test convolution rectangular extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular extension) : ", SNR_debruite)
            
            #On test convolution rectangular miroir
            image_debruitee = filtrage.filtrage_convolution_miroir("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular miroir) : ", SNR_debruite)
            
            #On test convolution rectangular wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau)
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution rectangular wrap) : ", SNR_debruite)
            
            #On test le filtre circular
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"circular")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution circular wrap) : ", SNR_debruite)
            
            #On test le filtre pyramidal
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"pyramidal")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution pyramidal wrap) : ", SNR_debruite)
            
            #On test le filtre cone
            #Crop
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone crop) : ", SNR_debruite)
            
            #Extension
            image_debruitee = filtrage.filtrage_convolution_extension("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone extension) : ", SNR_debruite)
            
            #Miroir
            image_debruitee = filtrage.filtrage_convolution_crop("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
            print("=== SNR de l'image débruitée (convolution cone miroir) : ", SNR_debruite)
            
            #Wrap
            image_debruitee = filtrage.filtrage_convolution_wrap("./images_reference/image_bruitee_test_salt_pepper.png",rayon_noyau,"cone")
            SNR_debruite = SNR.calcul_SNR(image_reference, image_debruitee)
            resultat_convolution.append(SNR_debruite)
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

    #On supprime les images créées
    os.remove("./images_reference/image_bruitee_test_multiplicatif.png")
    os.remove("./images_reference/image_bruitee_test_salt_pepper.png")
    os.remove("./images_reference/image_bruitee_test_additif.png")
    
    deinit() # pour arrêter colorama

def plot_three_noise_3d(kernel_sizes, noise_levels, methods, noisy_snr, filtered_snr, output_path=None):
    """
    Trace 3 surfaces/ensembles de courbes 3D, un subplot par type de bruit.

    Paramètres :
      - kernel_sizes : liste des tailles de noyau (ex. [3,5,7])
      - noise_levels : liste des niveaux de bruit (ex. ['faible','moyen','élevé'])
      - methods : liste des noms de méthodes (ex. ['median_crop','median_extension',...])
      - noisy_snr : dict bruit_type -> 1D array shape (len(noise_levels),)  (SNR de l'image bruitée par niveau)
      - filtered_snr : dict bruit_type -> dict method -> 2D array shape (len(noise_levels), len(kernel_sizes))
                       (SNR après filtrage pour chaque niveau et taille de noyau)
      - output_path : chemin de sauvegarde de la figure (optionnel)
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    bruit_types = list(filtered_snr.keys())  # ex. ['additif','multiplicatif','sel_poivre']
    fig = plt.figure(figsize=(18, 5))
    colors = plt.cm.tab10.colors

    for idx, bruit in enumerate(bruit_types):
        ax = fig.add_subplot(1, 3, idx+1, projection='3d')
        ax.set_title(f'Gain de SNR — bruit: {bruit}')
        ax.set_xlabel('Taille du noyau (px)')
        ax.set_ylabel('Niveau de bruit')
        ax.set_zlabel('Gain SNR (dB)')

        # grille X (kernel), Y (noise index)
        X = np.array(kernel_sizes)
        Y_vals = np.arange(len(noise_levels))

        noisy = np.asarray(noisy_snr[bruit])              # (N_levels,)
        # filtered_snr[bruit][method] -> shape (N_levels, N_kernels)
        for m_i, method in enumerate(methods):
            Z = np.asarray(filtered_snr[bruit][method])   # shape (N_levels, N_kernels)
            # gain = filtered - noisy (broadcast)
            gain = Z - noisy[:, None]                     # shape (N_levels, N_kernels)
            color = colors[m_i % len(colors)]
            label_plotted = False
            # pour chaque niveau de bruit, tracer la ligne le long des tailles de noyau
            for yi, y in enumerate(Y_vals):
                z_line = gain[yi, :]
                # n'afficher le label qu'une fois par méthode
                lbl = method if not label_plotted else None
                ax.plot(X, np.full_like(X, y), z_line, color=color, marker='o', label=lbl)
                label_plotted = True

        # remplacer ticks Y par labels lisibles
        ax.set_yticks(Y_vals)
        ax.set_yticklabels(noise_levels)
        ax.view_init(elev=30, azim=-60)
        ax.grid(True)

    # légende globale (méthodes)
    # crée un axe invisible pour placer la légende commune
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=min(len(methods), 6))
    plt.tight_layout(rect=[0,0,1,0.95])

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()
    plt.close(fig)