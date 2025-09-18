import numpy as np
import skimage as sk
import matplotlib.pyplot as plt

def filtrage_convolution_crop(chemin_image_bruitee, rayon_noyau):
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    if rayon_noyau==0:
        return image_bruitee
    else :
        diametre_noyau=2*rayon_noyau
    nb_ligne_img=image_bruitee.shape[0]
    nb_colonne_img=image_bruitee.shape[1]
    noyau=np.array([[0 for n in range(diametre_noyau)] for c in range(diametre_noyau)])
    for i in range(nb_ligne_img):
        for j in range(nb_colonne_img):
            if (i>=rayon_noyau and j>=rayon_noyau) and (i<nb_ligne_img-rayon_noyau and j<nb_colonne_img-rayon_noyau):
                for k in range(diametre_noyau):
                    for m in range(diametre_noyau):
                        noyau[k][m]=image_bruitee[i-rayon_noyau+k][j-rayon_noyau+m]
                image_bruitee[i][j]=np.sum(noyau)/noyau.size
    return image_bruitee

image_debruitee = filtrage_convolution_crop("./images_reference/image1_bruitee_snr_9.2885.png",3)
plt.imshow(image_debruitee, cmap="gray")
plt.show()
