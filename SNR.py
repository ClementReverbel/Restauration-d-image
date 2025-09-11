import numpy as np
import skimage as sk
import matplotlib.pyplot as plt

def calcul_SNR(chemin_image_base,chemin_image_bruitee) :
    #on recupere l'image sous form de matrice 
    image_original = sk.io.imread(chemin_image_base)
    image_bruitee = sk.io.imread(chemin_image_bruitee)
    p_signal = np.sum(image_original)
    p_bruit = np.sum(image_bruitee)$
    return 10 * np.log10(p_signal/p_bruit)

calcul_SNR("./images_reference/image_reference1.png","./images_reference/image1_bruitee_snr_9.2885.png")