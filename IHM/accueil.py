# coding: utf-8
import os
import sys
import importlib.util
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory

from IHM.clustering import ClusteringIHM
from IHM.reduction import ReductionIHM
from extraction import ouvrir_json

class AccueilIHM:
    def selectionner_fichier(self):
        if self.liste.curselection()[0] < 2:
            chemin = askopenfilename(filetypes=[('Fichier JSON', '*.json')])
            self.champ_fichier.config(state='normal')
            self.champ_fichier.delete(0, END)
            self.champ_fichier.insert(0, chemin)
            self.champ_fichier.config(state='readonly')
        else:
            script = self.liste_scripts[self.liste.curselection()[0] - 2]
            if len(script) < 3:
                chemin = askdirectory()
                self.champ_fichier.config(state='normal')
                self.champ_fichier.delete(0, END)
                self.champ_fichier.insert(0, chemin)
                self.champ_fichier.config(state='readonly')
            else:
                chemin = askopenfilename(filetypes=[(script[2], script[3])])
                self.champ_fichier.config(state='normal')
                self.champ_fichier.delete(0, END)
                self.champ_fichier.insert(0, chemin)
                self.champ_fichier.config(state='readonly')

    def peut_parcourir(self, message):
        self.bouton_parcourir.config(state='normal')

    def action(self):
        self.texte.set("Ouverture…")
        self.texte_label.config(fg='black')
        choix = -1
        chemin = self.champ_fichier.get()
        try:
            choix = self.liste.curselection()[0]
        except IndexError:
            self.texte.set("Veuillez sélectionner une action.")
            self.texte_label.config(fg='red')
        if choix == 0:
            try:
                data = ouvrir_json.charger_data([chemin])
                test = data[0]['nom']
                test = data[0]['image']
                test = data[0]['descripteurs']
                self.fenetre.destroy()
                ReductionIHM(data, chemin)
            except FileNotFoundError:
                self.texte.set("Aucun fichier sélectionné")
                self.texte_label.config(fg='red')
            except KeyError:
                self.texte.set("Fichier invalide")
                self.texte_label.config(fg='red')
        if choix == 1:
            try:
                data = ouvrir_json.charger_data([self.champ_fichier.get()])
                test = data[0]['nom']
                test = data[0]['image']
                test = data[0]['descripteurs']
                self.fenetre.destroy()
                ClusteringIHM(data, chemin)
            except FileNotFoundError:
                self.texte.set("Aucun fichier sélectionné")
                self.texte_label.config(fg='red')
            except KeyError:
                self.texte.set("Fichier invalide")
                self.texte_label.config(fg='red')
        if choix > 1:
            spec = importlib.util.spec_from_file_location(self.liste_scripts[choix - 2][1],
                                                          "../extraction/" + self.liste_scripts[choix - 2][1])
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            data = foo.charger_data([self.champ_fichier.get(), 20, "data.json"])  # TODO
            if len(data) > 0:
                self.fenetre.destroy()
                ReductionIHM(data, chemin + "/" + "data.json")
            else:
                self.texte.set("Aucune donnée trouvée")
                self.texte_label.config(fg='red')

    def __init__(self):
        self.fenetre = Tk()
        self.fenetre.title('Paralabe 2020 - Charger des données')
        self.texte = StringVar()
        self.couleur_texte = 'black'
        self.liste_scripts = []


        try:
            with open("../config.csv","r+", encoding='utf8') as fichier_config:
                lignes = fichier_config.readlines()
                for ligne in lignes:
                    self.liste_scripts.append(ligne.replace('\n', '').split(';'))
                if len(lignes)==0:
                    self.texte.set("Fichier config.csv vide")

        except FileNotFoundError:
            self.texte.set("Fichier config.csv introuvable")
            self.couleur_texte='red'

        self.conteneur_vertical = Frame(self.fenetre)
        self.conteneur_vertical.pack(side=TOP, fill=BOTH, pady=2, padx=2)
        self.liste = Listbox(self.conteneur_vertical, width=70, height=10)
        self.liste.bind('<<ListboxSelect>>', self.peut_parcourir)
        self.liste.insert(1, "Ouvrir un fichier de descripteurs pour la réduction")
        self.liste.insert(2, "Ouvrir un fichier de descripteurs pour le clustering")
        self.nombre_options=2
        for script in self.liste_scripts:
            self.nombre_options+=1
            self.liste.insert(self.nombre_options, script[0])
        self.liste.pack(side=TOP, fill=BOTH, pady=2, padx=2)

        self.conteneur_horizontal = Frame(self.conteneur_vertical, width=70)
        self.conteneur_horizontal.pack(side=TOP, fill=X, pady=2, padx=2)
        self.bouton_ok = Button(self.conteneur_horizontal, text="OK", width=10, command=self.action)
        self.bouton_ok.pack(side=RIGHT, fill=NONE, pady=2, padx=2)
        self.bouton_parcourir = Button(self.conteneur_horizontal, text="Parcourir", command=self.selectionner_fichier, width=10)
        self.bouton_parcourir.pack(side=RIGHT, fill=NONE, pady=2, padx=2)
        self.bouton_parcourir.config(state='disabled')
        self.champ_fichier = Entry(self.conteneur_horizontal, width=50)
        self.champ_fichier.config(state='readonly')
        self.champ_fichier.pack(side=RIGHT, fill=X, pady=2, padx=2)

        self.texte_label = Label(self.conteneur_vertical, textvariable=self.texte, anchor=E)
        self.texte_label.config(fg=self.couleur_texte)
        self.texte_label.pack(side=RIGHT, fill=NONE)

        self.fenetre.mainloop()

if __name__ == '__main__':
    sys.path.append(os.path.abspath(".."))
    AccueilIHM()