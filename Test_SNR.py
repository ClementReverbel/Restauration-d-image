import SNR
import bruit
import filtrage

import skimage as sk
import os

####################################################################################
#   
# Test des fonctions de filtrage sur du bruit additif
#
####################################################################################

if __name__ == '__main__':
    
    #Variables de test : 
    bruit_additif = 50
    bruit_multiplicatif = 0.5
    bruit_sel_et_poivre = (0.10,0.10)
    rayon_noyau = 2

    resultat_median=[]
    resultat_convolution=[]
    
    print("=== Test des fonctions de filtrage sur du bruit additif ===")
    image_reference = sk.io.imread("./images_reference/image_reference1.png")
    #A l'aide de l'image de référence, on génère une image bruitée
    #On l'a met dans une varaible & on la sauvegarde
    image_bruitee = bruit.bruit_additif("./images_reference/image_reference1.png", bruit_additif)
    sk.io.imsave("./images_reference/image1_bruitee_test_additif.png", image_bruitee)
    #On calcule le SNR entre l'image de référence et l'image bruitée
    SNR_bruité = SNR.calcul_SNR(image_reference, image_bruitee)
    print("=== SNR de l'image bruitée : ", SNR_bruité)
    
    #On fait des tests avec les différentes méthodes de filtrage
    
    #On test Crop
    #On teste median
    image_debruitee_crop = filtrage.filtrage_median_crop("./images_reference/image1_bruitee_test_additif.png",rayon_noyau)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    resultat_median.append(SNR_debruitee_crop)
    print("=== SNR de l'image débruitée (median crop) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_crop("./images_reference/image1_bruitee_test_additif.png",rayon_noyau)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    resultat_convolution.append(SNR_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution crop) : ", SNR_debruitee_extension)
    
    #On test extension
    #On test median
    image_debruitee_crop = filtrage.filtrage_median_extension("./images_reference/image1_bruitee_test_additif.png",rayon_noyau)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    resultat_median.append(SNR_debruitee_crop)
    print("=== SNR de l'image débruitée (median extension) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_extension("./images_reference/image1_bruitee_test_additif.png",rayon_noyau)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    resultat_convolution.append(SNR_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution extension) : ", SNR_debruitee_extension)
    
    #On test miroir
    #On test median
    image_debruitee_miroir = filtrage.filtrage_median_miroir("./images_reference/image1_bruitee_test_additif.png",rayon_noyau)
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    resultat_median.append(SNR_debruitee_miroir)
    print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruitee_miroir)
    
    #On test convolution
    image_debruitee_miroir = filtrage.filtrage_convolution_miroir("./images_reference/image1_bruitee_test_additif.png",rayon_noyau)
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    resultat_convolution.append(SNR_debruitee_miroir)
    print("=== SNR de l'image débruitée (convolution miroir) : ", SNR_debruitee_miroir)
    
    #On test wrap
    #On test median
    image_debruitee_wrap = filtrage.filtrage_median_wrap("./images_reference/image1_bruitee_test_additif.png",rayon_noyau)
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    resultat_median.append(SNR_debruitee_wrap)
    print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruitee_wrap)
    
    #On test convolution
    image_debruitee_wrap = filtrage.filtrage_convolution_wrap("./images_reference/image1_bruitee_test_additif.png",rayon_noyau)
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    resultat_convolution.append(SNR_debruitee_wrap)
    print("=== SNR de l'image débruitée (convolution wrap) : ", SNR_debruitee_wrap)
    
    #On supprime l'image créée
    os.remove("./images_reference/image1_bruitee_test_additif.png")

    print("\n=== Le meilleur résultat de SNR pour ce bruit avec un niveau de bruit additif de ",bruit_additif," et un rayon de ",rayon_noyau," pixels est : ")
    #On veut récupérer le max et l'indice pour afficher la méthode d'extension la meilleure
    max_median = max(resultat_median)
    indice_median = resultat_median.index(max_median)
    max_convolution = max(resultat_convolution)
    indice_convolution = resultat_convolution.index(max_convolution)
    if max_median > max_convolution :
        print("Median avec la méthode ",["Crop","Extension","Miroir","Wrap"][indice_median]," avec un SNR de : ",max_median)
    else :
        print("Convolution avec la méthode ",["Crop","Extension","Miroir","Wrap"][indice_convolution]," avec un SNR de : ",max_convolution)
    resultat_median.clear()
    resultat_convolution.clear()

####################################################################################
#   
# Test des fonctions de filtrage sur du bruit multiplicatif
#
####################################################################################

    print("\n\n")
    print("=== Test des fonctions de filtrage sur du bruit multiplicatif ===")
    image_reference = sk.io.imread("./images_reference/image_reference1.png")
    #A l'aide de l'image de référence, on génère une image bruitée
    #On l'a met dans une varaible & on la sauvegarde
    image_bruitee = bruit.bruit_multiplicatif("./images_reference/image_reference1.png", bruit_multiplicatif)
    sk.io.imsave("./images_reference/image1_bruitee_test_multiplicatif.png", image_bruitee)
    #On calcule le SNR entre l'image de référence et l'image bruitée
    SNR_bruité = SNR.calcul_SNR(image_reference, image_bruitee)
    print("=== SNR de l'image bruitée : ", SNR_bruité)
    
    #On fait des tests avec les différentes méthodes de filtrage
    
    #On test Crop
    #On teste median
    image_debruitee_crop = filtrage.filtrage_median_crop("./images_reference/image1_bruitee_test_multiplicatif.png",rayon_noyau)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    resultat_median.append(SNR_debruitee_crop)
    print("=== SNR de l'image débruitée (median crop) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_crop("./images_reference/image1_bruitee_test_multiplicatif.png",rayon_noyau)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    resultat_convolution.append(SNR_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution crop) : ", SNR_debruitee_extension)
    
    #On test extension
    #On test median
    image_debruitee_crop = filtrage.filtrage_median_extension("./images_reference/image1_bruitee_test_multiplicatif.png",rayon_noyau)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    resultat_median.append(SNR_debruitee_crop)
    print("=== SNR de l'image débruitée (median extension) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_extension("./images_reference/image1_bruitee_test_multiplicatif.png",rayon_noyau)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    resultat_convolution.append(SNR_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution extension) : ", SNR_debruitee_extension)
    
    #On test miroir
    #On test median
    image_debruitee_miroir = filtrage.filtrage_median_miroir("./images_reference/image1_bruitee_test_multiplicatif.png",rayon_noyau)
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    resultat_median.append(SNR_debruitee_miroir)
    print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruitee_miroir)
    
    #On test convolution
    image_debruitee_miroir = filtrage.filtrage_convolution_miroir("./images_reference/image1_bruitee_test_multiplicatif.png",rayon_noyau)
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    resultat_convolution.append(SNR_debruitee_miroir)
    print("=== SNR de l'image débruitée (convolution miroir) : ", SNR_debruitee_miroir)
    
    #On test wrap
    #On test median
    image_debruitee_wrap = filtrage.filtrage_median_wrap("./images_reference/image1_bruitee_test_multiplicatif.png",rayon_noyau)
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    resultat_median.append(SNR_debruitee_wrap)
    print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruitee_wrap)
    
    #On test convolution
    image_debruitee_wrap = filtrage.filtrage_convolution_wrap("./images_reference/image1_bruitee_test_multiplicatif.png",rayon_noyau)
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    resultat_convolution.append(SNR_debruitee_wrap)
    print("=== SNR de l'image débruitée (convolution wrap) : ", SNR_debruitee_wrap)
    
    #On supprime l'image créée
    os.remove("./images_reference/image1_bruitee_test_multiplicatif.png")
    
    print("\n=== Le meilleur résultat de SNR pour ce bruit avec un niveau de bruit multiplicatif de ",bruit_multiplicatif," et un rayon de ",rayon_noyau," pixels est : ")
    #On veut récupérer le max et l'indice pour afficher la méthode d'extension la meilleure
    max_median = max(resultat_median)
    indice_median = resultat_median.index(max_median)
    max_convolution = max(resultat_convolution)
    indice_convolution = resultat_convolution.index(max_convolution)
    if max_median > max_convolution :
        print("Median avec la méthode ",["Crop","Extension","Miroir","Wrap"][indice_median]," avec un SNR de : ",max_median)
    else :
        print("Convolution avec la méthode ",["Crop","Extension","Miroir","Wrap"][indice_convolution]," avec un SNR de : ",max_convolution)
    resultat_median.clear()
    resultat_convolution.clear()

####################################################################################
#   
# Test des fonctions de filtrage sur du bruit sel & poivre
#
####################################################################################

    print("\n\n")
    print("=== Test des fonctions de filtrage sur du bruit sel & poivre ===")
    image_reference = sk.io.imread("./images_reference/image_reference1.png")
    #A l'aide de l'image de référence, on génère une image bruitée
    #On l'a met dans une varaible & on la sauvegarde
    image_bruitee = bruit.bruit_salt_and_pepper("./images_reference/image_reference1.png",bruit_sel_et_poivre[0],bruit_sel_et_poivre[1])
    sk.io.imsave("./images_reference/image1_bruitee_test_salt_pepper.png", image_bruitee)
    #On calcule le SNR entre l'image de référence et l'image bruitée
    SNR_bruité = SNR.calcul_SNR(image_reference, image_bruitee)
    print("=== SNR de l'image bruitée : ", SNR_bruité)
    
    #On fait des tests avec les différentes méthodes de filtrage
    
    #On test Crop
    #On teste median
    image_debruitee_crop = filtrage.filtrage_median_crop("./images_reference/image1_bruitee_test_salt_pepper.png",rayon_noyau)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    resultat_median.append(SNR_debruitee_crop)
    print("=== SNR de l'image débruitée (median crop) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_crop("./images_reference/image1_bruitee_test_salt_pepper.png",rayon_noyau)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    resultat_convolution.append(SNR_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution crop) : ", SNR_debruitee_extension)
    
    #On test extension
    #On test median
    image_debruitee_crop = filtrage.filtrage_median_extension("./images_reference/image1_bruitee_test_salt_pepper.png",rayon_noyau)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    resultat_median.append(SNR_debruitee_crop)
    print("=== SNR de l'image débruitée (median extension) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_extension("./images_reference/image1_bruitee_test_salt_pepper.png",rayon_noyau)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    resultat_convolution.append(SNR_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution extension) : ", SNR_debruitee_extension)
    
    #On test miroir
    #On test median
    image_debruitee_miroir = filtrage.filtrage_median_miroir("./images_reference/image1_bruitee_test_salt_pepper.png",rayon_noyau)
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    resultat_median.append(SNR_debruitee_miroir)
    print("=== SNR de l'image débruitée (median miroir) : ", SNR_debruitee_miroir)
    
    #On test convolution
    image_debruitee_miroir = filtrage.filtrage_convolution_miroir("./images_reference/image1_bruitee_test_salt_pepper.png",rayon_noyau)
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    resultat_convolution.append(SNR_debruitee_miroir)
    print("=== SNR de l'image débruitée (convolution miroir) : ", SNR_debruitee_miroir)

    #On test wrap
    #On test median
    image_debruitee_wrap = filtrage.filtrage_median_wrap("./images_reference/image1_bruitee_test_salt_pepper.png",rayon_noyau)
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    resultat_median.append(SNR_debruitee_wrap)
    print("=== SNR de l'image débruitée (median wrap) : ", SNR_debruitee_wrap)
    
    #On test convolution
    image_debruitee_wrap = filtrage.filtrage_convolution_wrap("./images_reference/image1_bruitee_test_salt_pepper.png",rayon_noyau)
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    resultat_convolution.append(SNR_debruitee_wrap)
    print("=== SNR de l'image débruitée (convolution wrap) : ", SNR_debruitee_wrap)

    #On supprime l'image créée
    os.remove("./images_reference/image1_bruitee_test_salt_pepper.png")
    
    print("\n=== Le meilleur résultat de SNR pour ce bruit avec un niveau de bruit sel & poivre de probabilité respective : ",bruit_sel_et_poivre[0], ", ", bruit_sel_et_poivre[1]," et un rayon de ",rayon_noyau," pixels est : ")
    #On veut récupérer le max et l'indice pour afficher la méthode d'extension la meilleure
    max_median = max(resultat_median)
    indice_median = resultat_median.index(max_median)
    max_convolution = max(resultat_convolution)
    indice_convolution = resultat_convolution.index(max_convolution)
    if max_median > max_convolution :
        print("Median avec la méthode ",["Crop","Extension","Miroir","Wrap"][indice_median]," avec un SNR de : ",max_median)
    else :
        print("Convolution avec la méthode ",["Crop","Extension","Miroir","Wrap"][indice_convolution]," avec un SNR de : ",max_convolution)