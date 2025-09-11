import numpy as np
import skimage as sk
import matplotlib.pyplot as plt
from skimage.util import img_as_float   

def calcul_SNR(chemin_image_base, chemin_image_bruitee) :
    image_original = img_as_float(sk.io.imread(chemin_image_base))
    image_bruitee = img_as_float(sk.io.imread(chemin_image_bruitee))
    p_signal = np.sum(image_bruitee ** 2)
    p_bruit = np.sum((image_bruitee - image_original) ** 2)
    if p_bruit == 0:
        return float('inf')
    return 10 * np.log10(p_signal / p_bruit)

print(calcul_SNR("./images_reference/image_reference1.png","./images_reference/image1_bruitee_snr_10.8656.png"))