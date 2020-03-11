import umap
import numpy as np

from extraction.extractor_pixels import charger_data
from fonctions.autres import exporter_json

def reduire_dimensions(data, nom_entree, nom_sortie, n_neighbors, min_dist, n_components, path):
    vecteurs = []
    for i in data:
        vecteurs.append(i["descripteurs"][nom_entree])
    reducteur = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components)
    vecteurs_reduits = reducteur.fit_transform(vecteurs)
    for i in range(len(data)):
        data[i]["descripteurs"].update({nom_sortie : list(np.float64(vecteurs_reduits[i]))})
    exporter_json(path, "data.json", data)
    return data

if __name__ == '__main__':
    reduire_dimensions(charger_data(["../data/imagettes_paradiit/", 20]), "pixels", "2d", 100, 0.1, 2, "../data/imagettes_paradiit/")