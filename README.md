# Installation

* Télécharger le dossier
* Installer toutes les dépendances, avec pip ou conda
    * matplotlib
    * numpy
    * umap-learn
    * hdbscan

# Exécution

* Avec une IDE comme PyCharm : lancer exécuter le fichier Paralabe2020/IHM/accueil.py 
* Depuis la console, se placer dans le dossier IHM et exécuter le fichier accueil.py (cela ne marchera pas s'il est atteint depuis un autre dossier)

# Utilisation

* La fenêtre d'accueil permet de choisir les données d'entrée
* La fenêtre UMAP permet d'effectuer la réduction en choisissant les données d'entrée et quelques paramètres [(se référer à la documentation de UMAP)](https://umap-learn.readthedocs.io/en/latest/ "UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction")
    * Nombre de dimensions
    * n_neighbors
    * min_dist
    * Un nom pour les nouveaux descripteurs en dimensions réduites
* La fenêtre HDBSCAN permet d'effectuer le _clustering_ en choisissant les données d'entrée et deux paramètres [(se référer à la documentation de HDBSCAN)](https://hdbscan.readthedocs.io/en/latest/ "The hdbscan Clustering Library")
    * min_samples
    * Un nom pour le _clustering_

# Ajout de scripts d'extraction

La liste d'options pour choisir les données d'entrée dans la fenêtre d'accueil peut être augmentée sans modifier le code existant.
Il suffit pour cela de créer un nouveau fichier .py contenant une fonction appelée _charger_data_ et renvoyant un tableau de vecteurs conforme au [format utilisé par le programme](#format).
Elle devra être dans le dossier _extraction_ et, pour que le programme puisse l'utiliser, il faudra ajouter une ligne au fichier config.csv du dossier parent.
Cette ligne sera constituée de la description du nouveau mode d'entrée (affichée dans la fenêtre d'accueil), du nom du fichier.py, du type de fichiers utilisé par le mode d'entrée, et de l'extension correspondante, le tout séparé par des points-virgules.

Par exemple : `Créer les données à partir d'un fichier XML;extracteur_xml.py;Fichier XML;*.xml`

Dans le cas d'un mode d'entrée qui utilisé un dossier plutôt qu'un fichier, se contenter des deux premier éléments : `Produire des descripteurs à partir de la valeur des pixels;extracteur_pixels.py`

# <a href="#format"><a>Format utilisé par le programme

C'est un tableau de dictionnaires. Chaque dictionnaire représente un vecteur et est constitué ainsi :
* "nom": le nom du vecteur
* "image": une chaîne de caractères représentant l'image correspondante encodée en base64
* "descripteurs" : un dictionnaire, constitué d'autant de paires du type :
    * nom du descripteur : tableau de valeurs
    
Par exemple :
```json
[{       "nom": "image1",
       "image": "data:image/bmp;base64,Qk0m[...]AA==",
"descripteurs":
            { "nd": [255, 255, [...], 255],
              "2d":  [7.525875091552734, 2.7696139812469482]}},
[...]]
```