import hdbscan
import numpy as np
from datetime import datetime

from extraction.extractor_pixels import charger_data
from fonctions.autres import exporter_json
from fonctions.umap_reduction import reduire_dimensions


def clusteriser(data, nom_entree, nom_sortie, min_samples, path):
    date = datetime.now()
    nombre_dimensions = len(data[0]["descripteurs"][nom_entree])
    vecteurs = []
    clustering = {"description": "Clustering réalisé le "+date.strftime("%d/%m/%Y à %H:%M:%S")
                                + " à partir des descripteurs \""+nom_entree+" à "+str(nombre_dimensions)
                                + " dimensions du fichier data.json",
                  "clusters": {},
                  "tags": {}}
    for i in data:
        vecteurs.append(i["descripteurs"][nom_entree])
    clusterer = hdbscan.HDBSCAN(min_samples=min_samples)
    clusterer.fit(vecteurs)
    for i in range(len(data)):
        cluster = clusterer.labels_[i]
        if str(cluster) not in clustering["clusters"]:
            clustering["clusters"].update({str(cluster): []})
            clustering["tags"].update({str(cluster): []})
        clustering["clusters"][str(cluster)].append(data[i]["nom"])
    exporter_json(path, nom_sortie+".json", clustering)
    return clustering

if __name__ == '__main__':
    data = reduire_dimensions(charger_data(["../data/imagettes_paradiit/", 20]), "pixels", "2d", 100, 0.1, 2, "../data/imagettes_paradiit/")
    clusteriser(data, "2d", "clusters1", 10, "../data/imagettes_paradiit/")