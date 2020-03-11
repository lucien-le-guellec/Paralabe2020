import json
import os

def supprimer_descripteurs(chemin, nom):
    pass

def exporter_json(chemin, data):
    with open(os.path.join(chemin, "data.json"), "w+") as fichier:
        json_data = json.dumps(data)
        fichier.write(json_data)