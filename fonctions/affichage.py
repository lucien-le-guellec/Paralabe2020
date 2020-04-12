import matplotlib.pyplot as plt
import colorsys

def afficher(chemin, nom, data, clustering):
    """
    Affiche et enregistre la représentation graphique des points et des clusters
    :param chemin: le dossier qui contient les données
    :param nom: le nom du clustering, qui sera aussi celui de l'image
    :param data: le tableau des données
    :param clustering: le tableau du clustering
    :return: l'erreur éventuelle
    """
    n_clusters = len(clustering["clusters"])-1
    if clustering["dimensions"]!=2:
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