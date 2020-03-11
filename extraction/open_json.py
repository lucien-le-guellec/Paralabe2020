import json

def charger_data(args):
    with open(args[0], "r") as fichier_data:
        return json.loads(fichier_data.read())

if __name__ == '__main__':
    data = charger_data(["../data/imagettes_paradiit/data.json"])
    print (data[0])