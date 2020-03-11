import json
import os

def supprimer_descripteurs(chemin, nom):
    pass

def exporter_json(chemin, nom, data):
    with open(os.path.join(chemin, nom), "w+") as fichier:
        json_data = json.dumps(data)
        fichier.write(json_data)