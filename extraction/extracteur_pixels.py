import glob
import os
import base64
from PIL import Image
from fonctions.autres import exporter_json


def encoder_base64(fichier: str) -> str:
    """
    Permet d'obtenir la chaîne de caractère correspondant à l'image encorée en base64
    :param fichier: le chemin de l'image
    :return: la chaîne de caractère
    """
    with open(fichier, "rb") as fichier_image:
        fichier, ext = os.path.splitext(fichier)
        chaine_base64 = base64.b64encode(fichier_image.read()).decode()

    return f'data:image/{ext.replace(".", "")};base64,{chaine_base64}'

def charger_data(args):
    """
    Produit le tableau des données à partir d'un dossier d'images
    :param args: tableau d'arguments contenant le chemin du dossier, la taille de redimentionnement des images, et le nom du fichier à produire
    :return: le tableau des données
    """
    chemin = args[0]
    taille = args[1]
    nom_fichier = args[2]
    fichiers = []
    data = []


    nombre_fichiers_bmp = len(list(glob.glob(os.path.join(chemin, '*.bmp'))))
    nombre_fichiers_png = len(list(glob.glob(os.path.join(chemin, '*.png'))))
    nombre_fichiers_jpg = len(list(glob.glob(os.path.join(chemin, '*.jpg'))))

    num_files = nombre_fichiers_bmp + nombre_fichiers_png + nombre_fichiers_jpg

    for ext in ['*.bmp', '*.png', '*.jpg']:
        fichiers.extend(glob.glob(os.path.join(chemin, ext)))

    for i, infile in enumerate(fichiers):
        file, ext = os.path.splitext(infile)
        if ext == '.bmp' or ext == '.png' or ext == '.jpg':
            im = Image.open(infile)
            data_dict = {"nom": os.path.split(infile)[1],
                         "image": encoder_base64(infile),
                         "descripteurs": {"pixels": list(im.convert("L").resize((taille, taille)).getdata())}}
            data.append(data_dict)

    exporter_json(chemin, nom_fichier, data)

    return data