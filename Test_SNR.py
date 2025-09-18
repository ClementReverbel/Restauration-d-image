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
    print("=== Test des fonctions de filtrage sur du bruit additif ===")
    image_reference = sk.io.imread("./images_reference/image_reference1.png")
    #A l'aide de l'image de référence, on génère une image bruitée
    #On l'a met dans une varaible & on la sauvegarde
    image_bruitee = bruit.bruit_additif("./images_reference/image_reference1.png", 100)
    sk.io.imsave("./images_reference/image1_bruitee_test_additif.png", image_bruitee)
    #On calcule le SNR entre l'image de référence et l'image bruitée
    SNR_bruité = SNR.calcul_SNR(image_reference, image_bruitee)
    print("=== SNR de l'image bruitée : ", SNR_bruité)
    
    #On fait des tests avec les différentes méthodes de filtrage
    
    #On test Crop
    #On teste median
    image_debruitee_crop = filtrage.filtrage_median_crop("./images_reference/image1_bruitee_test_additif.png",5)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    print("=== SNR de l'image débruitée (median crop) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_crop("./images_reference/image1_bruitee_test_additif.png",5)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution crop) : ", SNR_debruitee_extension)
    
    #On test extension
    #On test median
    image_debruitee_crop = filtrage.filtrage_median_extension("./images_reference/image1_bruitee_test_additif.png",5)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    print("=== SNR de l'image débruitée (median extension) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_extension("./images_reference/image1_bruitee_test_additif.png",5)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution extension) : ", SNR_debruitee_extension)
    
    #On test miroir
    #On test median
    image_debruitee_miroir = filtrage.filtrage_median_miroir("./images_reference/image1_bruitee_test_additif.png")
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    print("=== SNR de l'image débruitée (miroir) : ", SNR_debruitee_miroir)
    
    #On test convolution
    image_debruitee_miroir = filtrage.filtrage_convolution_miroir("./images_reference/image1_bruitee_test_additif.png")
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    print("=== SNR de l'image débruitée (convolution miroir) : ", SNR_debruitee_miroir)
    
    #On test wrap
    #On test median
    image_debruitee_wrap = filtrage.filtrage_median_wrap("./images_reference/image1_bruitee_test_additif.png")
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    print("=== SNR de l'image débruitée (wrap) : ", SNR_debruitee_wrap)
    
    #On test convolution
    image_debruitee_wrap = filtrage.filtrage_convolution_wrap("./images_reference/image1_bruitee_test_additif.png")
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    print("=== SNR de l'image débruitée (convolution wrap) : ", SNR_debruitee_wrap)
    
    #On supprime l'image créée
    os.remove("./images_reference/image1_bruitee_test_additif.png")
    

####################################################################################
#   
# Test des fonctions de filtrage sur du bruit multiplicatif
#
####################################################################################

if __name__ == '__main__':
    print("\n\n")
    print("=== Test des fonctions de filtrage sur du bruit multiplicatif ===")
    image_reference = sk.io.imread("./images_reference/image_reference1.png")
    #A l'aide de l'image de référence, on génère une image bruitée
    #On l'a met dans une varaible & on la sauvegarde
    image_bruitee = bruit.bruit_multiplicatif("./images_reference/image_reference1.png", 0.5)
    sk.io.imsave("./images_reference/image1_bruitee_test_multiplicatif.png", image_bruitee)
    #On calcule le SNR entre l'image de référence et l'image bruitée
    SNR_bruité = SNR.calcul_SNR(image_reference, image_bruitee)
    print("=== SNR de l'image bruitée : ", SNR_bruité)
    
    #On fait des tests avec les différentes méthodes de filtrage
    
    #On test Crop
    #On teste median
    image_debruitee_crop = filtrage.filtrage_median_crop("./images_reference/image1_bruitee_test_multiplicatif.png",5)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    print("=== SNR de l'image débruitée (median crop) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_crop("./images_reference/image1_bruitee_test_multiplicatif.png",5)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution crop) : ", SNR_debruitee_extension)
    
    #On test extension
    #On test median
    image_debruitee_crop = filtrage.filtrage_median_extension("./images_reference/image1_bruitee_test_multiplicatif.png",5)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    print("=== SNR de l'image débruitée (median extension) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_extension("./images_reference/image1_bruitee_test_multiplicatif.png",5)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution extension) : ", SNR_debruitee_extension)
    
    #On test miroir
    #On test median
    image_debruitee_miroir = filtrage.filtrage_median_miroir("./images_reference/image1_bruitee_test_multiplicatif.png")
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    print("=== SNR de l'image débruitée (miroir) : ", SNR_debruitee_miroir)
    
    #On test convolution
    image_debruitee_miroir = filtrage.filtrage_convolution_miroir("./images_reference/image1_bruitee_test_multiplicatif.png")
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    print("=== SNR de l'image débruitée (convolution miroir) : ", SNR_debruitee_miroir)
    
    #On test wrap
    #On test median
    image_debruitee_wrap = filtrage.filtrage_median_wrap("./images_reference/image1_bruitee_test_multiplicatif.png")
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    print("=== SNR de l'image débruitée (wrap) : ", SNR_debruitee_wrap)
    
    #On test convolution
    image_debruitee_wrap = filtrage.filtrage_convolution_wrap("./images_reference/image1_bruitee_test_multiplicatif.png")
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    print("=== SNR de l'image débruitée (convolution wrap) : ", SNR_debruitee_wrap)
    
    #On supprime l'image créée
    os.remove("./images_reference/image1_bruitee_test_multiplicatif.png")

####################################################################################
#   
# Test des fonctions de filtrage sur du bruit sel & poivre
#
####################################################################################

if __name__ == '__main__':
    print("\n\n")
    print("=== Test des fonctions de filtrage sur du bruit sel & poivre ===")
    image_reference = sk.io.imread("./images_reference/image_reference1.png")
    #A l'aide de l'image de référence, on génère une image bruitée
    #On l'a met dans une varaible & on la sauvegarde
    image_bruitee = bruit.bruit_salt_and_pepper("./images_reference/image_reference1.png",0.10,0.10)
    sk.io.imsave("./images_reference/image1_bruitee_test_salt_pepper.png", image_bruitee)
    #On calcule le SNR entre l'image de référence et l'image bruitée
    SNR_bruité = SNR.calcul_SNR(image_reference, image_bruitee)
    print("=== SNR de l'image bruitée : ", SNR_bruité)
    
    #On fait des tests avec les différentes méthodes de filtrage
    
    #On test Crop
    #On teste median
    image_debruitee_crop = filtrage.filtrage_median_crop("./images_reference/image1_bruitee_test_salt_pepper.png",5)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    print("=== SNR de l'image débruitée (median crop) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_crop("./images_reference/image1_bruitee_test_salt_pepper.png",5)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution crop) : ", SNR_debruitee_extension)
    
    #On test extension
    #On test median
    image_debruitee_crop = filtrage.filtrage_median_extension("./images_reference/image1_bruitee_test_salt_pepper.png",5)
    SNR_debruitee_crop = SNR.calcul_SNR(image_reference, image_debruitee_crop)
    print("=== SNR de l'image débruitée (median extension) : ", SNR_debruitee_crop)
    
    #On test convolution
    image_debruitee_extension = filtrage.filtrage_convolution_extension("./images_reference/image1_bruitee_test_salt_pepper.png",5)
    SNR_debruitee_extension = SNR.calcul_SNR(image_reference, image_debruitee_extension)
    print("=== SNR de l'image débruitée (convolution extension) : ", SNR_debruitee_extension)
    
    #On test miroir
    #On test median
    image_debruitee_miroir = filtrage.filtrage_median_miroir("./images_reference/image1_bruitee_test_salt_pepper.png")
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    print("=== SNR de l'image débruitée (miroir) : ", SNR_debruitee_miroir)
    
    #On test convolution
    image_debruitee_miroir = filtrage.filtrage_convolution_miroir("./images_reference/image1_bruitee_test_salt_pepper.png")
    SNR_debruitee_miroir = SNR.calcul_SNR(image_reference, image_debruitee_miroir)
    print("=== SNR de l'image débruitée (convolution miroir) : ", SNR_debruitee_miroir)

    #On test wrap
    #On test median
    image_debruitee_wrap = filtrage.filtrage_median_wrap("./images_reference/image1_bruitee_test_salt_pepper.png")
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    print("=== SNR de l'image débruitée (wrap) : ", SNR_debruitee_wrap)
    
    #On test convolution
    image_debruitee_wrap = filtrage.filtrage_convolution_wrap("./images_reference/image1_bruitee_test_salt_pepper.png")
    SNR_debruitee_wrap = SNR.calcul_SNR(image_reference, image_debruitee_wrap)
    print("=== SNR de l'image débruitée (convolution wrap) : ", SNR_debruitee_wrap)

    #On supprime l'image créée
    os.remove("./images_reference/image1_bruitee_test_salt_pepper.png")