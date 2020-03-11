import os

import umap
import numpy as np

from extraction.extracteur_pixels import charger_data
from fonctions.autres import exporter_json

def reduire_dimensions(data, nom_entree, nom_sortie, n_neighbors, min_dist, n_components, chemin):
    vecteurs = []
    for i in data:
        vecteurs.append(i["descripteurs"][nom_entree])
    reducteur = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components)
    vecteurs_reduits = reducteur.fit_transform(vecteurs)
    for i in range(len(data)):
        data[i]["descripteurs"].update({nom_sortie : list(np.float64(vecteurs_reduits[i]))})
    dossier, fichier = os.path.split(chemin)
    exporter_json(dossier, fichier, data)
    return data

if __name__ == '__main__':
    reduire_dimensions(charger_data(["../data/imagettes_paradiit/", 20, "data.json"]), "pixels", "2d", 100, 0.1, 2, "../data/imagettes_paradiit/data.json")