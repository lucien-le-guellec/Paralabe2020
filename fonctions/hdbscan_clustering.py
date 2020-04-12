import hdbscan
from datetime import datetime

from fonctions.autres import exporter_json


def clusteriser(data, nom_entree, nom_sortie, min_samples, path, nom_fichier):
    """
    Produit des clusters pour les vecteurs, avec l'algorithme HDBSCAN
    :param data: le tableau des données
    :param nom_entree: le nom du descripteur à utiliser
    :param nom_sortie: le nom du fichier qui contiendra le clustering
    :param min_samples: la valeur du paramètre min_samples de l'algorithme HDBSCAN
    :param path: le dossier contenant les données
    :param nom_fichier: le fichier contenant les données utilisées pour le clustering
    :return: le tableau contenant les clusters
    """
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