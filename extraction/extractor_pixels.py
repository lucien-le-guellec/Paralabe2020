import glob
import json
import os
import base64
from PIL import Image

def exporter_json(chemin, data):
    with open(os.path.join(chemin, "data.json"), "w+") as fichier:
        json_data = json.dumps(data)
        fichier.write(json_data)

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
    path = args[0]
    size = args[1]
    # Variables declaration
    files = []
    data = []

    # Open a json file and write data into it
    #with open(os.path.join(path, "data.json"), "w+") as outfile:


    num_files_bmp = len(list(glob.glob(os.path.join(path, '*.bmp'))))
    num_files_png = len(list(glob.glob(os.path.join(path, '*.png'))))
    num_files_jpg = len(list(glob.glob(os.path.join(path, '*.jpg'))))

    num_files = num_files_bmp + num_files_png + num_files_jpg

    # Random printings
    print("Working directory :", path)
    print("Number of BMP files :", num_files_bmp)
    print("Number of PNG files :", num_files_png)
    print("Number of JPG files :", num_files_jpg)

    # print_progress_bar(0, num_files, prefix='Progress:', suffix='Complete', length=50)

    # Get all the files with the given extensions in the directory set in argv
    for ext in ['*.bmp', '*.png', '*.jpg']:
        files.extend(glob.glob(os.path.join(path, ext)))

    # Gets the greyscale of the images
    # Put data into a json file
    for i, infile in enumerate(files):
        file, ext = os.path.splitext(infile)
        if ext == '.bmp' or ext == '.png' or ext == '.jpg':
            im = Image.open(infile)
            data_dict = {"nom": os.path.split(infile)[1],
                         "image": encoder_base64(infile),
                         "descripteurs": {"pixels": list(im.convert("L").resize((size, size)).getdata())}}
            data.append(data_dict)
        # print_progress_bar(i + 1, num_files, prefix='Progress:', suffix='Complete', length=50)

    exporter_json(path, data)

    # Summary printing
    print(f"Process as successfully ended !\n{num_files} "
          f"files have been exported into {os.path.join(path, 'data.json')}.\n")

    return data

if __name__ == '__main__':
    charger_data(["../data/imagettes_paradiit/", 20])