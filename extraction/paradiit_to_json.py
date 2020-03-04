import glob
import json
import os
import xml.etree.ElementTree as ETree
import argparse
import base64
from PIL import Image


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Print a console progress bar
    :param iteration: the current iteration
    :param total: total iterations
    :param prefix: text before the progress bar
    :param suffix: text after the progress bar
    :param decimals: the number of decimals for the percent completion
    :param length: size of the progress bar in character
    :param fill: the progress bar filling character
    :return: print a progress bar to the given state
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('{} |{}| {}% {}'.format(prefix, bar, percent, suffix), end="\r")
    if iteration == total:
        print('\n')


def encode_to_base64(file: str) -> str:
    """
    Encode an image into a base64 string
    :param file: the path to the image
    :return: an encoded base64 string of the given image
    """

    with open(file, "rb") as image_file:
        file, ext = os.path.splitext(file)
        encoded_string = base64.b64encode(image_file.read()).decode()

    return f'data:image/{ext.replace(".", "")};base64,{encoded_string}'


def export_to_json(args):
    """
    Export all necessaries data of an image folder into a json file
    :param args: program arguments
    :return: create a data.json file
    """

    for path in args.DIR:

        # Variables declaration
        files = []
        width = 20
        length = 20
        conversion_mode = "1"
        if args.greyscale:
            conversion_mode = "L"
        data_dict = dict(data=[],
                         target=[],
                         img_data=[],
                         feature_names=[f"Pixel{s}" for s in range(width * length)],
                         DESCR="Paradiit project data"
                               "\nThese are images data representing characters from ancient books.")

        # Open a json file and write data into it
        with open(os.path.join(path, "data.json"), "w") as outfile:

            if args.recursive:
                num_files_bmp = len(list(glob.glob(os.path.join(path, '**/*.bmp'), recursive=True)))
                num_files_png = len(list(glob.glob(os.path.join(path, '**/*.png'), recursive=True)))
                num_files_jpg = len(list(glob.glob(os.path.join(path, '**/*.jpg'), recursive=True)))
                num_files_xml = len(list(glob.glob(os.path.join(path, '**/*.xml'), recursive=True)))
            else:
                num_files_bmp = len(list(glob.glob(os.path.join(path, '*.bmp'))))
                num_files_png = len(list(glob.glob(os.path.join(path, '*.png'))))
                num_files_jpg = len(list(glob.glob(os.path.join(path, '*.jpg'))))
                num_files_xml = len(list(glob.glob(os.path.join(path, '*.xml'))))

            num_files = num_files_bmp + num_files_png + num_files_jpg + num_files_xml

            # Random printings
            print("Working directory :", path)
            print("Number of BMP files :", num_files_bmp)
            print("Number of PNG files :", num_files_png)
            print("Number of JPG files :", num_files_jpg)
            print("Number of XML files :", num_files_xml)

            print_progress_bar(0, num_files, prefix='Progress:', suffix='Complete', length=50)

            # Get all the files with the given extensions in the directory set in argv
            for ext in ['*.bmp', '*.png', '*.jpg', '*.xml']:
                if args.recursive:
                    files.extend(glob.glob(os.path.join(path, '**/' + ext), recursive=True))
                else:
                    files.extend(glob.glob(os.path.join(path, ext)))

            # Gets the greyscale of the images with the corresponding target ascii character
            # Put data into a json file
            for i, infile in enumerate(files):
                file, ext = os.path.splitext(infile)
                if ext == '.bmp' or ext == '.png' or ext == '.jpg':
                    im = Image.open(infile)
                    data_dict['data'].append(list(im.convert(conversion_mode).resize((width, length)).getdata()))
                    data_dict['img_data'].append(encode_to_base64(infile))
                if ext == '.xml':
                    root = ETree.parse(infile).getroot()
                    data_dict['target'].append(root.find('Label').get('ascii'))
                print_progress_bar(i + 1, num_files, prefix='Progress:', suffix='Complete', length=50)

            json_data_dict = json.dumps(data_dict)
            outfile.write(json_data_dict)

            # Summary printing
            print(f"Process as successfully ended !\n{num_files} "
                  f"files have been exported into {os.path.join(path, 'data.json')}.\n")


if __name__ == '__main__':
    # Handle programs arguments
    parser = argparse.ArgumentParser(
        description="Paradiit dataset to JSON (v0.5) by Y. GALAN"
                    "\nGet the pixels of all the images in the given directory and export them into a JSON file."
                    "\nIf the corresponding XML file exists, add the image OCR target in the JSON string."
                    "\nImage format accepted : BMP, PNG, JPG",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("DIR", help="the path to the working directory", nargs='*', type=str)
    parser.add_argument("-r", "--recursive", help="include sub-directories", action="store_true")
    parser.add_argument("-m", "--monochrome", help="convert images in 1-bit monochrome (default)", action="store_true")
    parser.add_argument("-g", "--greyscale", help="convert images in 8-bit greyscale", action="store_true")
    parser_args = parser.parse_args()

    # Welcome printing
    print("\nParadiit dataset to JSON (v0.5) by Y. GALAN"
          "\nUsage: paradiit_to_json.py [-h] [-r] [-m] [-g] [DIR [DIR ...]]\n"
          "\nGet the pixels of all the images in the given directory and parse them into a JSON file."
          "\nIf exists, add the image OCR target in the JSON string."
          "\nImage format accepted : BMP, PNG, JPG\n")

    export_to_json(parser_args)
