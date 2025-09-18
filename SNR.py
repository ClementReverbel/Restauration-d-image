import numpy as np
import skimage as sk
import matplotlib.pyplot as plt
from skimage.util import img_as_float   

#Calcul du SNR entre une image de référence et une image bruitée
def calcul_SNR(chemin_image_base, chemin_image_bruitee) :
    #on recupere les images sous forme de matrice
    image_original = img_as_float(sk.io.imread(chemin_image_base))
    image_bruitee = img_as_float(sk.io.imread(chemin_image_bruitee))
    #on calcule la puissance du signal et du bruit
    p_signal = np.sum(image_bruitee ** 2)
    p_bruit = np.sum((image_bruitee - image_original) ** 2)
    #on gère le cas où le bruit est nul (même image)
    if p_bruit == 0:
        return float('inf')
    #on calcule le SNR en dB
    return 10 * np.log10(p_signal / p_bruit)

print(calcul_SNR("./images_reference/image_reference1.png","./images_reference/image1_bruitee_snr_10.8656.png"))