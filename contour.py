import numpy as np
import skimage as sk
import matplotlib.pyplot as plt

import filtrage

####################################################################################################
#
# Fonctions génériques de filtrage (Canny)
#
####################################################################################################

def filtrage_canny(image,seuil_bas,seuil_haut):
    #On utilise le filtre extension par défault
    image = np.pad(image, pad_width=1, mode='edge')
    
    #On prépare nos filtres d'après la méthode de Canny
    #Masques Sobel
    masque_horizontal = np.array([[-1, 0, 1],
                                  [-2, 0, 2],
                                  [-1, 0, 1]])
    masque_vertical   = np.array([[-1, -2, -1],
                                  [ 0,  0,  0],
                                  [ 1,  2,  1]])
    gradient_horizontal=np.array([])
    gradient_vertical=np.array([])
    
    nb_ligne_img=len(image)
    nb_colonne_img=len(image[0])
    
    masque_contour=image.copy()
    
    #On parcout l'image
    for i in range(nb_ligne_img):
        for j in range(nb_colonne_img):
            if (i>=1 and j>=1) and (i<nb_ligne_img-1 and j<nb_colonne_img-1):
                #On récupère les valeurs des pixels pour appliquer le filtre
                gradient_horizontal=image[i-1:i+2,j-1:j+2]
                gradient_vertical=image[i-1:i+2,j-1:j+2]
                gradient_horizontal=np.sum(gradient_horizontal*masque_horizontal)
                gradient_vertical=np.sum(gradient_vertical*masque_vertical)
                #On fait le calcul de la mangitude
                magnitude_gradient=np.sqrt(gradient_horizontal**2+gradient_vertical**2)
                #Pour chaque pixel on vérifie avec le seuil_bas/haut
                if magnitude_gradient<seuil_bas:
                    masque_contour[i][j]=0
                elif magnitude_gradient>seuil_haut:
                    masque_contour[i][j]=255
                else:
                    #Permet de définir ceux qui sont entre les deux
                    masque_contour[i][j]=1
    
    for i in range(nb_ligne_img):
        for j in range(nb_colonne_img):
            if (i>=1 and j>=1) and (i<nb_ligne_img-1 and j<nb_colonne_img-1):
                if masque_contour[i][j]==1:
                    for m in range(-1,2):
                        for n in range(-1,2):
                            if masque_contour[m+i][n+j]==255:
                                masque_contour[i][j]=255
                                break
                
    masque_contour = masque_contour[1:-1, 1:-1]
    return masque_contour

#Après plusieurs tests, les valeurs 112 et 225 s'apparantent être
#les plus optimales dans le cas de nos images en nuance de gris
def application_contours(image_base,image_debruitee,seuil_bas=112,seuil_haut=225):
    masque_contour=filtrage_canny(image_debruitee,seuil_bas,seuil_haut)
    for i in range(len(masque_contour)):
        for j in range(len(masque_contour[0])):
            if masque_contour[i][j]==255:
                image_debruitee[i][j]=image_base[i][j]
    return image_debruitee

if __name__=="__main__":
    img_base=sk.io.imread("./images_reference/image1_bruitee_snr_9.2885.png")
    img=filtrage.filtrage_convolution_extension("./images_reference/image1_bruitee_snr_9.2885.png",2,"pyramidal")
    
    img=filtrage_canny(img,80,200)
    plt.imshow(img, cmap="gray")
    plt.show()