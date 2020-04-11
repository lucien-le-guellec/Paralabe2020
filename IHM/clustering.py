import os
from tkinter import *
from tkinter.ttk import Combobox

from fonctions.affichage import afficher
from fonctions.hdbscan_clustering import clusteriser


class ClusteringIHM:
    def lancer_clustering(self):
        if len(self.champ_nom.get())<1:
            self.texte.set('Veuillez entrer un nom.')
            self.texte_label.config(fg='red')
        else:
            try:
                self.texte.set('Opération en cours…')
                self.texte_label.config(fg='black')
                dossier, fichier = os.path.split(self.nom_fichier)
                clustering = clusteriser(self.data, self.liste_entrees.get().split(' (')[0], self.champ_nom.get(), int(self.selecteur_min_samples.get()), dossier, fichier)
                afficher(dossier+'/', self.champ_nom.get(), self.data, clustering)
                nombre_clusters = str(len(clustering['clusters']))
                self.texte.set('Clustering enregistré dans le fichier '+self.champ_nom.get()+'.json ('+nombre_clusters+' clusters)')
            except KeyError:
                self.texte.set('Veuillez choisir un descripteur.')
                self.texte_label.config(fg='red')

    def retour(self):
        self.fenetre.destroy()
        from IHM.reduction import ReductionIHM
        ReductionIHM(self.data, self.nom_fichier)

    def __init__(self, d, c):
        self.data = d
        self.nom_fichier = c
        self.fenetre = Tk()
        self.fenetre.title('Paralabe 2020 - HDBSCAN')
        self.texte = StringVar()
        self.entrees = list(self.data[0]['descripteurs'].keys())
        for i in range(len(self.entrees)):
            self.entrees[i] += ' (' + str(len(self.data[0]['descripteurs'][self.entrees[i]])) + ' dimensions)'

        self.nombre_vecteurs = len(self.data)

        # conteneur_2_col
        self.conteneur_2_col = Frame(self.fenetre)
        self.conteneur_2_col.pack(side=TOP, fill=BOTH, pady=2, padx=2)
        #    conteneur_gauche
        self.conteneur_gauche = Frame(self.conteneur_2_col)
        self.conteneur_gauche.pack(side=LEFT, fill=BOTH, pady=2, padx=2)
        #        texte_fichier
        self.texte_fichier = Label(self.conteneur_gauche, text="Fichier sélectionné : " + self.nom_fichier)
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
        #    conteneur_droit
        self.conteneur_droit = Frame(self.conteneur_2_col)
        self.conteneur_droit.pack(side=LEFT, fill=BOTH, pady=2, padx=2)
        #        texte_vecteurs
        self.texte_vecteurs = Label(self.conteneur_droit, text="Vecteurs : " + str(self.nombre_vecteurs))
        self.texte_vecteurs.pack(anchor=E, side=TOP, fill=NONE, pady=2, padx=2)

        #        bouton_lancer
        self.bouton_lancer = Button(self.conteneur_droit, text="Lancer le clustering", command=self.lancer_clustering)
        self.bouton_lancer.pack(anchor=S, side=BOTTOM, fill=NONE, pady=2, padx=2)
        #        conteneur_nom
        self.conteneur_nom = Frame(self.conteneur_droit)
        self.conteneur_nom.pack(anchor=E, side=BOTTOM, fill=BOTH, pady=2, padx=2)
        #            texte_nom
        self.texte_nom = Label(self.conteneur_nom, text='Nom du clustering :')
        self.texte_nom.pack(side=LEFT, anchor=N, fill=NONE)
        #            champ_nom
        self.champ_nom = Entry(self.conteneur_nom, width=20)
        self.champ_nom.pack(side=RIGHT, anchor=N, fill=X, pady=2, padx=2)
        #        conteneur_min_samples
        self.conteneur_min_samples = Frame(self.conteneur_droit)
        self.conteneur_min_samples.pack(anchor=E, side=BOTTOM, fill=BOTH, pady=2, padx=2)
        #            texte_min_samples
        self.texte_min_samples = Label(self.conteneur_min_samples, text='min_samples :')
        self.texte_min_samples.pack(side=LEFT, anchor=N, fill=NONE)
        #            selecteur_min_samples
        self.selecteur_min_samples = Spinbox(self.conteneur_min_samples, from_=1, to=10000)
        self.selecteur_min_samples.delete(0, END)
        self.selecteur_min_samples.insert(0, 10)
        self.selecteur_min_samples.pack(side=RIGHT, anchor=N, fill=NONE)
        #        titre_droit
        self.titre_droit = Label(self.conteneur_droit, text='Sorties :', font='TkDefaultFont 9 bold')
        self.titre_droit.pack(side=BOTTOM, anchor=W, fill=NONE)
        # texte
        self.texte_label = Label(self.fenetre, textvariable=self.texte)
        self.texte_label.pack(side=RIGHT, anchor=N, fill=NONE)

        self.fenetre.mainloop()