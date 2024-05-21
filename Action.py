import tkinter as tk

from parametre import NOM_BOUTONS, COULEUR_CORPS

#actions ->   quelques boutons : recuperer disponibilité (et met dans archive), calculer emploi du temps (dirige ensuite sur visionner, et selectionne par defaut un des emplois calculé),
#             envoyer message sur discord (via un bot surement) pour montrer le planning, mise en ligne du tableur de demande de dispo et copie du lien dans le presse papier,
#             envoie message sur discord pour la demande de dispo

class Action():
    def __init__(self, root) -> None:
        self.root = root

        self.dessinerBouton()
    
    def dessinerBouton(self):
        x = self.root.winfo_width()//2
        y = self.root.winfo_height()//2
        pad = int(y/100*3)

        frame = tk.Frame(self.root, background=COULEUR_CORPS)
        frame.place(anchor="center", x=x,y=y)

        listeBoutons = []
        for i in range(len(NOM_BOUTONS)):
            nom = NOM_BOUTONS[i]

            bouton = tk.Button(frame, text=nom, font="liberation 20", border=6)
            bouton.pack(pady=(pad,pad))
            listeBoutons.append(bouton)

        listeBoutons[0].config(command=lambda:self.recupDispo())
        listeBoutons[1].config(command=lambda:self.calculPlanning())
        listeBoutons[2].config(command=lambda:self.envoiePlanning())
        listeBoutons[3].config(command=lambda:self.creerDemande())
        listeBoutons[4].config(command=lambda:self.envoieDemande())
    
    def recupDispo(self):
        print("dispo recupéré")
    
    def calculPlanning(self):
        print("planning calculé")
    
    def envoiePlanning(self):
        print("planning envoyé")
    
    def creerDemande(self):
        print("demande créée")
    
    def envoieDemande(self):
        print("demande envoyé")
