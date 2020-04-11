import os
from tkinter import *
from tkinter.ttk import Combobox

from IHM.clustering import ClusteringIHM
from fonctions.autres import supprimer_descripteurs
from fonctions.umap_reduction import reduire_dimensions


class ReductionIHM:
    
    def lancer_reduction(self):
        if len(self.champ_nom.get())<1:
            self.texte.set('Veuillez entrer un nom.')
            self.texte_label.config(fg='red')
        else:
            try:
                self.texte.set('Opération en cours…')
                self.texte_label.config(fg='black')
                data = reduire_dimensions(self.data, self.liste_entrees.get().split(' (')[0], self.champ_nom.get(), int(self.selecteur_n_neighbors.get()), float(self.selecteur_min_dist.get()), int(self.selecteur_dimensions.get()), self.nom_fichier)
                self.fenetre.destroy()
                ClusteringIHM(data, self.nom_fichier)
            except KeyError:
                self.texte.set('Veuillez choisir un descripteur.')
                self.texte_label.config(fg='red')

    def supprimer(self):
        try:
            self.texte.set('Opération en cours…')
            self.texte_label.config(fg='black')
            dossier, fichier = os.path.split(self.nom_fichier)
            data = supprimer_descripteurs(dossier, fichier, self.liste_entrees.get().split(' (')[0], self.data)
            self.fenetre.destroy()
            ReductionIHM(data, self.nom_fichier)
        except KeyError:
            self.texte.set('Veuillez choisir un descripteur.')
            self.texte_label.config(fg='red')

    def passer(self):
        self.fenetre.destroy()
        ClusteringIHM(self.data, self.nom_fichier)

    def retour(self):
        self.fenetre.destroy()
        from IHM.accueil import AccueilIHM
        AccueilIHM()
    
    def __init__(self, d, c):

        self.data = d
        self.nom_fichier = c
        self.fenetre = Tk()
        self.fenetre.title('Paralabe 2020 - UMAP')
        self.texte = StringVar()
        self.entrees = list(self.data[0]['descripteurs'].keys())
        self.nombre_dimensions = []
        for i in range(len(self.entrees)):
            nd = len(self.data[0]['descripteurs'][self.entrees[i]])
            self.nombre_dimensions.append(nd)
            self.entrees[i] += ' (' + str(nd) + ' dimensions)'

        self.nombre_vecteurs = len(self.data)


        #conteneur_2_col
        self.conteneur_2_col = Frame(self.fenetre)
        self.conteneur_2_col.pack(side=TOP, fill=BOTH, pady=2, padx=2)
        #    conteneur_gauche
        self.conteneur_gauche = Frame(self.conteneur_2_col)
        self.conteneur_gauche.pack(side=LEFT, fill=BOTH, pady=2, padx=2)
        #        texte_fichier
        self.texte_fichier = Label(self.conteneur_gauche, text="Fichier sélectionné : "+self.nom_fichier)
        self.texte_fichier.pack(anchor=W, side=TOP, fill=NONE, pady=2, padx=2)
        #        bouton_retour
        self.bouton_retour = Button(self.conteneur_gauche, text="Retour", command=self.retour, width=10)
        self.bouton_retour.pack(anchor=W, side=TOP, fill=NONE, pady=2, padx=2)
        #        titre_gauche
        self.titre_gauche = Label(self.conteneur_gauche, text='Entrées :', font='TkDefaultFont 9 bold')
        self.titre_gauche.pack(side=TOP, anchor=W, fill=NONE)
        #        liste_entrees
        self.liste_entrees = Combobox(self.conteneur_gauche, values=self.entrees)
        self.liste_entrees.pack(side=TOP, anchor=W, fill=NONE)
        #        bouton_supprimer
        self.bouton_supprimer = Button(self.conteneur_gauche, text="Supprimer ces descripteurs", command=self.supprimer)
        self.bouton_supprimer.pack(side=BOTTOM, anchor=S, fill=NONE, pady=2, padx=2)
        #    conteneur_droit
        self.conteneur_droit = Frame(self.conteneur_2_col)
        self.conteneur_droit.pack(side=LEFT, fill=BOTH, pady=2, padx=2)
        #        texte_vecteurs
        self.texte_vecteurs = Label(self.conteneur_droit, text="Vecteurs : "+str(self.nombre_vecteurs))
        self.texte_vecteurs.pack(anchor=E, side=TOP, fill=NONE, pady=2, padx=2)
        #        bouton_clustering
        self.bouton_clustering = Button(self.conteneur_droit, text="Passer directement au clustering", command=self.passer, width=35)
        self.bouton_clustering.pack(anchor=E, side=TOP, fill=NONE, pady=2, padx=2)
        #        titre_droit
        self.titre_droit = Label(self.conteneur_droit, text='Sorties :', font='TkDefaultFont 9 bold')
        self.titre_droit.pack(side=TOP, anchor=W, fill=NONE)
        #        conteneur_dimensions
        self.conteneur_dimensions = Frame(self.conteneur_droit)
        self.conteneur_dimensions.pack(anchor=E, side=TOP, fill=BOTH, pady=2, padx=2)
        #            texte_dimensions
        self.texte_dimensions = Label(self.conteneur_dimensions, text='Nombre de dimensions :')
        self.texte_dimensions.pack(side=LEFT, anchor=N, fill=NONE)
        #            selecteur_dimensions
        self.selecteur_dimensions = Spinbox(self.conteneur_dimensions, from_=1, to=max(self.nombre_dimensions))
        self.selecteur_dimensions.delete(0, END)
        self.selecteur_dimensions.insert(0, 2)
        self.selecteur_dimensions.pack(side=RIGHT, anchor=N, fill=NONE)
        #        conteneur_n_neighbors
        self.conteneur_n_neighbors = Frame(self.conteneur_droit)
        self.conteneur_n_neighbors.pack(anchor=E, side=TOP, fill=BOTH, pady=2, padx=2)
        #            texte_n_neighbors
        self.texte_n_neighbors = Label(self.conteneur_n_neighbors, text='n_neighbors :')
        self.texte_n_neighbors.pack(side=LEFT, anchor=N, fill=NONE)
        #            selecteur_n_neighbors
        self.selecteur_n_neighbors = Spinbox(self.conteneur_n_neighbors, from_=1, to=10000)
        self.selecteur_n_neighbors.delete(0, END)
        self.selecteur_n_neighbors.insert(0, 100)
        self.selecteur_n_neighbors.pack(side=RIGHT, anchor=N, fill=NONE)
        #        conteneur_min_dist
        self.conteneur_min_dist = Frame(self.conteneur_droit)
        self.conteneur_min_dist.pack(anchor=E, side=TOP, fill=BOTH, pady=2, padx=2)
        #            texte_min_dist
        self.texte_min_dist = Label(self.conteneur_min_dist, text='min_dist :')
        self.texte_min_dist.pack(side=LEFT, anchor=N, fill=NONE)
        #            selecteur_min_dist
        self.selecteur_min_dist = Spinbox(self.conteneur_min_dist, from_=0, to=1, increment=0.001)
        self.selecteur_min_dist.delete(0, END)
        self.selecteur_min_dist.insert(0, 0.1)
        self.selecteur_min_dist.pack(side=RIGHT, anchor=N, fill=NONE)
        #        conteneur_nom
        self.conteneur_nom = Frame(self.conteneur_droit)
        self.conteneur_nom.pack(anchor=E, side=TOP, fill=BOTH, pady=2, padx=2)
        #            texte_nom
        self.texte_nom = Label(self.conteneur_nom, text='Nom du descripteur :')
        self.texte_nom.pack(side=LEFT, anchor=N, fill=NONE)
        #            champ_nom
        self.champ_nom = Entry(self.conteneur_nom, width=20)
        self.champ_nom.pack(side=RIGHT, anchor=N, fill=X, pady=2, padx=2)
        #bouton_lancer
        self.bouton_lancer = Button(self.fenetre, text="Lancer la réduction", command=self.lancer_reduction)
        self.bouton_lancer.pack(anchor=N, side=TOP, fill=NONE, pady=2, padx=2)
        #texte
        self.texte_label = Label(self.fenetre, textvariable=self.texte)
        self.texte_label.pack(side=RIGHT, anchor=N, fill=NONE)


        self.fenetre.mainloop()


