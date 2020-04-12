import os
import umap
import numpy as np

from fonctions.autres import exporter_json

def reduire_dimensions(data, nom_entree, nom_sortie, n_neighbors, min_dist, n_components, chemin):
    """
    Produit un nouveau descripteur pour les vecteurs, avec moins de dimensions, grâge à l'algorithme UMAP
    :param data: le tableau des données
    :param nom_entree: le nom du descripteur utilisé
    :param nom_sortie: le nom du nouveau descripteur
    :param n_neighbors: la valeur du paramètre n_neighbors de l'algorithme UMAP
    :param min_dist: la valeur du paramètre min_dist de l'algorithme UMAP
    :param n_components: le nombre de dimensions souhaité pour le nouveau descripteur
    :param chemin: le chemin vers le fichier contenant les données
    :return:
    """
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