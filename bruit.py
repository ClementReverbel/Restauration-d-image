import numpy as np
import skimage as sk
import matplotlib.pyplot as plt


    
    



#bruiter avec un bruit additif
def bruit_additif(chemin_image, niveau_bruit):
    #on recupere l'image sous form de matrice 
    image = sk.io.imread(chemin_image)
    #on crée un bruit de la même taille que l'image avec un niveau de bruit donné
    bruit = np.random.normal(0, niveau_bruit, image.shape)
    #on ajoute le bruit à l'image
    return image + bruit

image_bruitee = bruit_additif("./images_reference/image_reference1.png", 100)
plt.imshow(image_bruitee, cmap="gray")
plt.show()

#bruiter avec un bruit multiplicatif
def bruit_multiplicatif(chemin_image, niveau_bruit):
    #on recupere l'image sous form de matrice
    image = sk.io.imread(chemin_image)
    #on crée un bruit de la même taille que l'image avec un niveau de bruit donné
    bruit = np.random.normal(0, niveau_bruit, image.shape)
    #on ajoute le bruit à l'image
    return image * (1 + bruit)

image_bruitee = bruit_multiplicatif("./images_reference/image_reference1.png", 0.5)
plt.imshow(image_bruitee, cmap="gray")
plt.show()
