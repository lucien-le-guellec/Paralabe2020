import matplotlib.pyplot as plt
import json

from extraction.extracteur_pixels import charger_data
from fonctions.hdbscan_clustering import clusteriser
from fonctions.umap_reduction import reduire_dimensions


def afficher(chemin, clustering):
    data = charger_data([chemin+clustering["fichier"]])

if __name__ == '__main__':
    data = reduire_dimensions(charger_data(["../data/imagettes_paradiit/", 20, "data.json"]), "pixels", "2d", 100, 0.1, 2, "../data/imagettes_paradiit/data.json")
    afficher(clusteriser(data, "2d", "clusters1", 10, "../data/imagettes_paradiit/", "data.json"))