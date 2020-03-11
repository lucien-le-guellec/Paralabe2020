import glob
import os
import base64
from PIL import Image
from fonctions.autres import exporter_json


def encoder_base64(fichier: str) -> str:
    with open(fichier, "rb") as fichier_image:
        fichier, ext = os.path.splitext(fichier)
        chaine_base64 = base64.b64encode(fichier_image.read()).decode()

    return f'data:image/{ext.replace(".", "")};base64,{chaine_base64}'

def charger_data(args):
    chemin = args[0]
    taille = args[1]
    nom_fichier = args[2]
    files = []
    data = []


    nombre_fichiers_bmp = len(list(glob.glob(os.path.join(chemin, '*.bmp'))))
    nombre_fichiers_png = len(list(glob.glob(os.path.join(chemin, '*.png'))))
    nombre_fichiers_jpg = len(list(glob.glob(os.path.join(chemin, '*.jpg'))))

    num_files = nombre_fichiers_bmp + nombre_fichiers_png + nombre_fichiers_jpg

    # print("Working directory :", chemin)
    # print("Number of BMP files :", nombre_fichiers_bmp)
    # print("Number of PNG files :", nombre_fichiers_png)
    # print("Number of JPG files :", nombre_fichiers_jpg)

    # print_progress_bar(0, num_files, prefix='Progress:', suffix='Complete', length=50)
    for ext in ['*.bmp', '*.png', '*.jpg']:
        files.extend(glob.glob(os.path.join(chemin, ext)))

    # Gets the greyscale of the images
    # Put data into a json file
    for i, infile in enumerate(files):
        file, ext = os.path.splitext(infile)
        if ext == '.bmp' or ext == '.png' or ext == '.jpg':
            im = Image.open(infile)
            data_dict = {"nom": os.path.split(infile)[1],
                         "image": encoder_base64(infile),
                         "descripteurs": {"pixels": list(im.convert("L").resize((taille, taille)).getdata())}}
            data.append(data_dict)
        # print_progress_bar(i + 1, num_files, prefix='Progress:', suffix='Complete', length=50)

    exporter_json(chemin, nom_fichier, data)

    # print(f"Process as successfully ended !\n{num_files} "
    #       f"files have been exported into {os.path.join(chemin, 'data.json')}.\n")

    return data

if __name__ == '__main__':
    charger_data(["../data/imagettes_paradiit/", 20, "data.json"])