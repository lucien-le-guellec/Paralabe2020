import umap
import numpy as np

from extraction.extractor_pixels import charger_data
from fonctions.autres import exporter_json

def reduire_dimensions(data, nom_entree, nom_sortie, path):
    vecteurs = []
    for i in data:
        vecteurs.append(i["descripteurs"][nom_entree])
    reducteur = umap.UMAP()
    vecteurs_reduits = reducteur.fit_transform(vecteurs)
    for i in range(len(data)):
        data[i]["descripteurs"].update({nom_sortie : list(np.float64(vecteurs_reduits[i]))})
    exporter_json(path, data)
    return data

if __name__ == '__main__':
    reduire_dimensions(charger_data(["../data/imagettes_paradiit/", 20]), "pixels", "2d", "../data/imagettes_paradiit/")