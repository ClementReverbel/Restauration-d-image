import numpy as np
import skimage as sk
import matplotlib.pyplot as plt

####################################################################################################
#
# Fonctions de création de matrice de filtres
#
###################################################################################################

def ligne_pyramide(i, rayon):
    # partie croissante
    croissant = [j * i for j in range(1, rayon)]
    # partie décroissante
    decroissant = [j * i for j in range(rayon, 0, -1)]
    return croissant + decroissant

def matrice_pyramide(rayon):
    rayon+=1
    masque_noyau = [ligne_pyramide(i, rayon) for i in range(1, rayon)]
    masque_noyau += [ligne_pyramide(i, rayon) for i in range(rayon, 0, -1)]
    return masque_noyau

def matrice_circulaire(rayon):
    size = 2 * rayon + 1  # matrice carrée de dimension impaire
    masque = np.zeros((size, size), dtype=int)
    
    for i in range(size):
        for j in range(size):
            # distance au centre
            if (i - rayon)**2 + (j - rayon)**2 <= rayon**2:
                masque[i, j] = 1
    return masque


def matrice_cone(rayon):
    size = 2 * rayon + 1  # matrice carrée de dimension impaire
    masque = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            # distance au centre
            if (i - rayon)**2 + (j - rayon)**2 <= rayon**2:
                masque[i, j] = rayon**2-((i - rayon)**2 + (j - rayon)**2)+1
    return masque

####################################################################################################
#
# Fonctions génériques de filtrage (médian et par convolution)
#
####################################################################################################

#Fonction prennant en paramètre une image bruitée et un rayon de noyau, et renvoyant l'image filtrée par convolution
def filtrage_convolution(image_bruitee, rayon_noyau, nom_filtre="rectangular"):        
    #Si le rayon du noyau est nul, on ne fait rien
    if rayon_noyau==0:
        return image_bruitee
    else :
        diametre_noyau=2*rayon_noyau
        
    #Vérification du nom du filtre
    if not nom_filtre in ["rectangular","circular","pyramidal","cone"]:
        raise ValueError("Le nom du filtre doit être 'rectangular', 'circular', 'pyramidal' ou 'cone'")

    masque_noyau=[]
    #Selon le type de filtre, on crée le masque du noyau
    match nom_filtre:
        case "rectangular":
            masque_noyau=np.array([[1 for n in range(diametre_noyau+1)] for c in range(diametre_noyau+1)])
        case "circular":
            masque_noyau=matrice_circulaire(rayon_noyau)
        case "pyramidal":
            masque_noyau=np.array(matrice_pyramide(rayon_noyau))
        case "cone":
            masque_noyau=np.array(matrice_cone(rayon_noyau))
    #On initialise les variables
    nb_ligne_img=image_bruitee.shape[0]
    nb_colonne_img=image_bruitee.shape[1]
    nouvelle_image=image_bruitee.copy()
    noyau=np.array([])
    
    

    #On parcourt l'image
    if image_bruitee.ndim == 3:
        nb_canaux = image_bruitee.shape[2]
        for c in range(nb_canaux):
            for i in range(rayon_noyau, nb_ligne_img - rayon_noyau):
                for j in range(rayon_noyau, nb_colonne_img - rayon_noyau):
                    noyau = image_bruitee[i-rayon_noyau:i+rayon_noyau+1,
                                          j-rayon_noyau:j+rayon_noyau+1, c]
                    nouvelle_image[i, j, c] = np.sum(noyau * masque_noyau) / np.sum(masque_noyau)
    else:
        for i in range(rayon_noyau, nb_ligne_img - rayon_noyau):
            for j in range(rayon_noyau, nb_colonne_img - rayon_noyau):
                noyau = image_bruitee[i-rayon_noyau:i+rayon_noyau+1,
                                      j-rayon_noyau:j+rayon_noyau+1]
                nouvelle_image[i, j] = np.sum(noyau * masque_noyau) / np.sum(masque_noyau)
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
    if image_bruitee.ndim == 3:
        nb_canaux = image_bruitee.shape[2]
        nouvelle_image = image_bruitee.copy()
        for c in range(nb_canaux):
            for i in range(rayon_noyau, nb_ligne_img - rayon_noyau):
                for j in range(rayon_noyau, nb_colonne_img - rayon_noyau):
                    noyau = image_bruitee[i-rayon_noyau:i+rayon_noyau+1,
                                          j-rayon_noyau:j+rayon_noyau+1, c]
                    nouvelle_image[i, j, c] = np.median(noyau)
    else:
        nouvelle_image = image_bruitee.copy()
        for i in range(rayon_noyau, nb_ligne_img - rayon_noyau):
            for j in range(rayon_noyau, nb_colonne_img - rayon_noyau):
                noyau = image_bruitee[i-rayon_noyau:i+rayon_noyau+1,
                                      j-rayon_noyau:j+rayon_noyau+1]
                nouvelle_image[i, j] = np.median(noyau)
    return nouvelle_image


####################################################################################################
#
# Fonctions de filtrage par convolution avec gestion des bords (crop, extension, miroir, wrap)
#
####################################################################################################

#Fonction de filtrage par convolution avec gestion des bords (crop)
def filtrage_convolution_crop(chemin_image_bruitee,rayon_noyau,nom_filtre="rectangular"):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    return filtrage_convolution(image_bruitee, rayon_noyau,nom_filtre)

#Fonction de filtrage par convolution avec gestion des bords (extension)
def filtrage_convolution_extension(chemin_image_bruitee,rayon_noyau,nom_filtre="rectangular"):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'edge' (pixels de bord répétés)
    # pad_width est une tuple pour appliquer le padding différemment par dimension
    if image_bruitee.ndim == 3:
        pad_width = ((rayon_noyau, rayon_noyau), (rayon_noyau, rayon_noyau), (0, 0))
    else:
        pad_width = rayon_noyau
    image_bruitee = np.pad(image_bruitee, pad_width=pad_width, mode='edge')
    image_bruitee = filtrage_convolution(image_bruitee, rayon_noyau,nom_filtre)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

#Fonction de filtrage par convolution avec gestion des bords (miroir)
def filtrage_convolution_miroir(chemin_image_bruitee,rayon_noyau,nom_filtre="rectangular"):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'symmetric' (pixel extérieur répétant le pixel intérieur)
    if image_bruitee.ndim == 3:
        pad_width = ((rayon_noyau, rayon_noyau), (rayon_noyau, rayon_noyau), (0, 0))
    else:
        pad_width = rayon_noyau
    image_bruitee = np.pad(image_bruitee, pad_width=pad_width, mode='symmetric')
    image_bruitee = filtrage_convolution(image_bruitee, rayon_noyau,nom_filtre)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

#Fonction de filtrage par convolution avec gestion des bords (wrap)
def filtrage_convolution_wrap(chemin_image_bruitee,rayon_noyau,nom_filtre="rectangular"):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'wrap' (pixels du bord opposé)
    if image_bruitee.ndim == 3:
        pad_width = ((rayon_noyau, rayon_noyau), (rayon_noyau, rayon_noyau), (0, 0))
    else:
        pad_width = rayon_noyau
    image_bruitee = np.pad(image_bruitee, pad_width=pad_width, mode='wrap')
    image_bruitee = filtrage_convolution(image_bruitee, rayon_noyau,nom_filtre)
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
    if image_bruitee.ndim == 3:
        pad_width = ((rayon_noyau, rayon_noyau), (rayon_noyau, rayon_noyau), (0, 0))
    else:
        pad_width = rayon_noyau
    image_bruitee = np.pad(image_bruitee, pad_width=pad_width, mode='edge')
    image_bruitee = filtrage_median(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

#Fonction de filtrage médian avec gestion des bords (miroir)
def filtrage_median_miroir(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'symmetric' (pixel extérieur répétant le pixel intérieur)
    if image_bruitee.ndim == 3:
        pad_width = ((rayon_noyau, rayon_noyau), (rayon_noyau, rayon_noyau), (0, 0))
    else:
        pad_width = rayon_noyau
    image_bruitee = np.pad(image_bruitee, pad_width=pad_width, mode='symmetric')
    image_bruitee = filtrage_median(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

#Fonction de filtrage médian avec gestion des bords (wrap)
def filtrage_median_wrap(chemin_image_bruitee,rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    # On étend l'image en utilisant la méthode 'wrap' (pixels du bord opposé)
    if image_bruitee.ndim == 3:
        pad_width = ((rayon_noyau, rayon_noyau), (rayon_noyau, rayon_noyau), (0, 0))
    else:
        pad_width = rayon_noyau
    image_bruitee = np.pad(image_bruitee, pad_width=pad_width, mode='wrap')
    image_bruitee = filtrage_median(image_bruitee, rayon_noyau)
    image_bruitee = image_bruitee[rayon_noyau:-rayon_noyau, rayon_noyau:-rayon_noyau]
    return image_bruitee

####################################################################################################
#
# Utilisation des fonctions
#
####################################################################################################

if __name__ == '__main__':
    image_debruitee = filtrage_convolution_extension("./images_reference/image3_reference.png",2)
    plt.imshow(image_debruitee, cmap="gray")
    plt.show()
