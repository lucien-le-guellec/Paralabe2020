import glob
import os
import base64
from PIL import Image
from fonctions.autres import exporter_json


def encoder_base64(fichier: str) -> str:
    """
    Encode an image into a base64 string
    :param fichier: the path to the image
    :return: an encoded base64 string of the given image
    """

    with open(fichier, "rb") as fichier_image:
        fichier, ext = os.path.splitext(fichier)
        chaine_base64 = base64.b64encode(fichier_image.read()).decode()

    return f'data:image/{ext.replace(".", "")};base64,{chaine_base64}'

def charger_data(args):
    chemin = args[0]
    taille = args[1]
    # Variables declaration
    files = []
    data = []

    # Open a json file and write data into it
    #with open(os.path.join(path, "data.json"), "w+") as outfile:


    nombre_fichiers_bmp = len(list(glob.glob(os.path.join(chemin, '*.bmp'))))
    nombre_fichiers_png = len(list(glob.glob(os.path.join(chemin, '*.png'))))
    nombre_fichiers_jpg = len(list(glob.glob(os.path.join(chemin, '*.jpg'))))

    num_files = nombre_fichiers_bmp + nombre_fichiers_png + nombre_fichiers_jpg

    # Random printings
    print("Working directory :", chemin)
    print("Number of BMP files :", nombre_fichiers_bmp)
    print("Number of PNG files :", nombre_fichiers_png)
    print("Number of JPG files :", nombre_fichiers_jpg)

    # print_progress_bar(0, num_files, prefix='Progress:', suffix='Complete', length=50)

    # Get all the files with the given extensions in the directory set in argv
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

    exporter_json(chemin, "data.json", data)

    # Summary printing
    print(f"Process as successfully ended !\n{num_files} "
          f"files have been exported into {os.path.join(chemin, 'data.json')}.\n")

    return data

if __name__ == '__main__':
    charger_data(["../data/imagettes_paradiit/", 20])