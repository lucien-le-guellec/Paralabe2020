import matplotlib.pyplot as plt
import colorsys

from extraction.extracteur_pixels import charger_data as cd1
from extraction.ouvrir_json import charger_data
from fonctions.hdbscan_clustering import clusteriser
from fonctions.umap_reduction import reduire_dimensions


def afficher(chemin, nom, clustering):
    data = charger_data([chemin+clustering["fichier"]])
    n_clusters = len(clustering["clusters"])-1
    if clustering["dimensions"]>2:
        return "Affichage impossible avec plus de deux dimensions"
    else:
        x = []
        y = []
        couleurs = []
        for i in data:
            if i["nom"] in clustering["clusters"]["-1"]:
                x.append(i["descripteurs"][clustering["descripteurs"]][0])
                y.append(i["descripteurs"][clustering["descripteurs"]][1])
                couleurs.append((0.8, 0.8, 0.8))
            else:
                for j in range(n_clusters):
                    if i["nom"] in clustering["clusters"][str(j)]:
                        x.append(i["descripteurs"][clustering["descripteurs"]][0])
                        y.append(i["descripteurs"][clustering["descripteurs"]][1])
                        couleurs.append(colorsys.hsv_to_rgb(1/(n_clusters)*j,1,1))
        plt.scatter(x, y, c=couleurs, s=0.1)
        plt.rcParams["axes.titlesize"] = 8
        plt.title(clustering["description"])
        plt.savefig(chemin+nom+".png")
        plt.show()

if __name__ == '__main__':
    data = reduire_dimensions(cd1(["../data/imagettes_paradiit/", 20, "data.json"]), "pixels", "2d", 100, 0.1, 2, "../data/imagettes_paradiit/data.json")
    afficher("../data/imagettes_paradiit/", "clusters1", clusteriser(data, "2d", "clusters1", 10, "../data/imagettes_paradiit/", "data.json"))