import json

def charger_data(args):
    """
    Ouvre un fichier de vecteurs et insère les données dans un tableau
    :param args: un tableau contenant le chemin du fichier
    :return: le tableau des données
    """
    with open(args[0], "r") as fichier_data:
        return json.loads(fichier_data.read())