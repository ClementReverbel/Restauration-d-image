import numpy as np
import skimage as sk
import matplotlib.pyplot as plt

####################################################################################################
#
# Fonctions génériques de filtrage (médian et par convolution)
#
####################################################################################################

#Fonction prennant en paramètre une image bruitée et un rayon de noyau, et renvoyant l'image filtrée par convolution
def filtrage_convolution(image_bruitee, rayon_noyau):
    #Si le rayon du noyau est nul, on ne fait rien
    if rayon_noyau==0:
        return image_bruitee
    else :
        diametre_noyau=2*rayon_noyau
    #On initialise les variables
    nb_ligne_img=image_bruitee.shape[0]
    nb_colonne_img=image_bruitee.shape[1]
    nouvelle_image=image_bruitee.copy()
    noyau=np.array([[0 for n in range(diametre_noyau)] for c in range(diametre_noyau)])
    #On parcourt l'image
    for i in range(nb_ligne_img):
        for j in range(nb_colonne_img):
            #On ne traite que les pixels pour lesquels le noyau est entièrement dans l'image
            if (i>=rayon_noyau and j>=rayon_noyau) and (i<nb_ligne_img-rayon_noyau and j<nb_colonne_img-rayon_noyau):
                #On parcourt chaque pixel du noyau
                for k in range(diametre_noyau):
                    for m in range(diametre_noyau):
                        #On remplit le noyau avec les valeurs de l'image
                        noyau[k][m]=image_bruitee[i-rayon_noyau+k][j-rayon_noyau+m]
                # On calcule la moyenne du noyau
                nouvelle_image[i][j]=np.sum(noyau)/noyau.size
    return nouvelle_image

#Fonction prennant en paramètre une image bruitée et un rayon de noyau, et renvoyant l'image filtrée par médiane
def filtrage_median(image_bruitee, rayon_noyau):
    #Si le rayon du noyau est nul, on ne fait rien
    if rayon_noyau==0:
        return image_bruitee
    else :
        diametre_noyau=2*rayon_noyau
    #On initialise les variables
    nb_ligne_img=image_bruitee.shape[0]
    nb_colonne_img=image_bruitee.shape[1]
    nouvelle_image=image_bruitee.copy()
    noyau=np.array([[0 for n in range(diametre_noyau)] for c in range(diametre_noyau)])
    #On parcourt l'image
    for i in range(nb_ligne_img):
        for j in range(nb_colonne_img):
            #On ne traite que les pixels pour lesquels le noyau est entièrement dans l'image
            if (i>=rayon_noyau and j>=rayon_noyau) and (i<nb_ligne_img-rayon_noyau and j<nb_colonne_img-rayon_noyau):
                #On parcourt chaque pixel du noyau
                for k in range(diametre_noyau):
                    for m in range(diametre_noyau):
                        #On remplit le noyau avec les valeurs de l'image
                        noyau[k][m]=image_bruitee[i-rayon_noyau+k][j-rayon_noyau+m]
                # On calcule la médiane du noyau
                nouvelle_image[i][j]=np.median(noyau)
    return nouvelle_image


####################################################################################################
#
# Fonctions de filtrage par convolution avec gestion des bords (crop, extension, miroir, wrap)
#
####################################################################################################

#Fonction de filtrage par convolution avec gestion des bords (crop)
def filtrage_convolution_crop(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    return filtrage_convolution(image_bruitee, rayon_noyau)

#Fonction de filtrage par convolution avec gestion des bords (extension)
def filtrage_convolution_extension(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'edge' (pixels de bord répétés)
    image_bruitee = np.pad(image_bruitee, pad_width=rayon_noyau, mode='edge')
    image_bruitee = filtrage_convolution(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

#Fonction de filtrage par convolution avec gestion des bords (miroir)
def filtrage_convolution_miroir(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'symmetric' (pixel extérieur répétant le pixel intérieur)
    image_bruitee = np.pad(image_bruitee, pad_width=rayon_noyau, mode='symmetric')
    image_bruitee = filtrage_convolution(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

#Fonction de filtrage par convolution avec gestion des bords (wrap)
def filtrage_convolution_wrap(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'wrap' (pixels du bord opposé)
    image_bruitee = np.pad(image_bruitee, pad_width=rayon_noyau, mode='wrap')
    image_bruitee = filtrage_convolution(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

####################################################################################################
#
# Filtrage médian avec gestion des bords (crop, extension, miroir, wrap)
#
####################################################################################################

#Fonction de filtrage médian avec gestion des bords (crop)
def filtrage_median_crop(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    return filtrage_median(image_bruitee, rayon_noyau)

#Fonction de filtrage médian avec gestion des bords (extension)
def filtrage_median_extension(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'edge' (pixels de bord répétés)
    image_bruitee = np.pad(image_bruitee, pad_width=rayon_noyau, mode='edge')
    image_bruitee = filtrage_median(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

#Fonction de filtrage médian avec gestion des bords (miroir)
def filtrage_median_miroir(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'symmetric' (pixel extérieur répétant le pixel intérieur)
    image_bruitee = np.pad(image_bruitee, pad_width=rayon_noyau, mode='symmetric')
    image_bruitee = filtrage_median(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

#Fonction de filtrage médian avec gestion des bords (wrap)
def filtrage_median_wrap(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'wrap' (pixels du bord opposé)
    image_bruitee = np.pad(image_bruitee, pad_width=rayon_noyau, mode='wrap')
    image_bruitee = filtrage_median(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

####################################################################################################
#
# Utilisation des fonctions
#
####################################################################################################

if __name__ == '__main__':
    image_debruitee = filtrage_median_crop("./images_reference/image1_bruitee_snr_9.2885.png",5)
    plt.imshow(image_debruitee, cmap="gray")
    plt.show()
