import json
import os

def supprimer_descripteurs(chemin, nom_fichier, nom_descripteur, data):
    """
    Permet de supprimer un descripteur dans le tableau des données et le fichier correspondant
    :param chemin: le dossier contenant le fichier
    :param nom_fichier: le nom du fichier
    :param nom_descripteur: le nom du descripteur à supprimer
    :param data: le tableau des données
    :return: le tableau avec un descripteur en moins
    """
    for i in data:
        del i["descripteurs"][nom_descripteur]
    exporter_json(chemin, nom_fichier, data)
    return data

def exporter_json(chemin, nom, data):
    """
    Permet d'écrire le tableau des données dans un fichier JSON
    :param chemin: le dossier contenant le fichier
    :param nom: le nom du fichier à écrire
    :param data: le tableau des données
    """
    with open(os.path.join(chemin, nom), "w+", encoding='utf8') as fichier:
        json_data = json.dumps(data)
        fichier.write(json_data)
