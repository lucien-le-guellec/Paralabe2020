import json

def charger_data(args):
    with open(args[0], "r") as fichier_data:
        return json.loads(fichier_data.read())