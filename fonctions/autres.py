import json
import os

from extraction.ouvrir_json import charger_data


def supprimer_descripteurs(chemin, nom_fichier, nom_descripteur, data):
    for i in data:
        del i["descripteurs"][nom_descripteur]
    exporter_json(chemin, nom_fichier, data)
    pass

def exporter_json(chemin, nom, data):
    with open(os.path.join(chemin, nom), "w+", encoding='utf8') as fichier:
        json_data = json.dumps(data)
        fichier.write(json_data)

if __name__ == '__main__':
    supprimer_descripteurs("../data/imagettes_paradiit/", "data.json", "pixels", charger_data(["../data/imagettes_paradiit/data.json"]))