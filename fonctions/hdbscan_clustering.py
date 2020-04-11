import hdbscan
from datetime import datetime

from extraction.extracteur_pixels import charger_data
from fonctions.autres import exporter_json
from fonctions.umap_reduction import reduire_dimensions


def clusteriser(data, nom_entree, nom_sortie, min_samples, path, nom_fichier):
    date = datetime.now()
    nombre_dimensions = len(data[0]["descripteurs"][nom_entree])
    vecteurs = []
    for i in data:
        vecteurs.append(i["descripteurs"][nom_entree])
    clusterer = hdbscan.HDBSCAN(min_samples=min_samples)
    clusterer.fit(vecteurs)
    clustering = {"description": "Clustering fait le "+date.strftime("%d/%m/%Y, %H:%M:%S")
                                + ", depuis les descripteurs \""+nom_entree+"\" ("+str(nombre_dimensions)
                                + " dimensions) \n du fichier "+nom_fichier+", avec min_samples = "+str(min_samples),
                  "fichier": nom_fichier,
                  "descripteurs": nom_entree,
                  "dimensions": nombre_dimensions,
                  "min_samples": min_samples,
                  "clusters": {},
                  "tags": {}}
    for i in range(len(data)):
        cluster = clusterer.labels_[i]
        if str(cluster) not in clustering["clusters"]:
            clustering["clusters"].update({str(cluster): []})
            clustering["tags"].update({str(cluster): []})
        clustering["clusters"][str(cluster)].append(data[i]["nom"])
    exporter_json(path, nom_sortie+".json", clustering)
    return clustering