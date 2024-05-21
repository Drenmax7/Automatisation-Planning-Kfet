import tkinter as tk

from parametre import HAUTEUR_MENU, NOM_ONGLETS

#kfetier ->   tableau montrant tout les kfetier, permet la modification de leurs informations, d'en rajouter, d'en supprimer
#             genere le exel permettant de demander les dispo lors de la sauvegarde
#visionner -> affiche un des emploi du temps calculé, met en evidence les personnes ayant plusieurs services (ou en decalage par rapport aux autres)
#             et permet de circuler parmis les emplois du temps calculé afin d'en choisir un, et permet une modification facile des noms attribué,
#             possede un bouton selectionner qui enregistre l'emploi du temps actuel comme etant celui selectionné, en cree une image et la met dans le presse papier
#             montrer la date et heure du planning
#actions ->   quelques boutons : recuperer disponibilité, calculer emploi du temps (dirige ensuite sur visionner, et selectionne par defaut un des emplois calculé),
#             envoyer message sur discord (via un bot surement) pour montrer le planning, mise en ligne du tableur de demande de dispo et copie du lien dans le presse papier,
#             envoie message sur discord pour la demande de dispo
#spe jour ->  permet de changer les jours et periode pour lesquels il faut attribuer des gens, les effectifs par periode, effectif generaux (change egalement les effectif specifique)
#
#option ->    gerer les identifiants du compte google pour exel, les identifiants du bot pour envoyer les messages discord, 
#             modifier le contenu du message automatique (avec possibilité de ping), le salon dans lequel le message est envoyé, 
#             taille batch d'emploi du temps (dans l'algo de calcul, combien sont gardé par etape), 
#             conditions speciale (des gens qui ne peuvent pas regulierement sur certains jours)

class Menu():
    def __init__(self, menu):
        self.menu = menu
        self.ongletActuel = "Actions"
    
    def redefinirTaille(self, width):
        self.menu.config(width=width)

    def creerFonction(self,nom):
        return lambda _: self.changeOnglet(nom)

    def changeOnglet(self, nom):
        self.ongletActuel = nom
        self.corps.dessinerOnglet(self.ongletActuel)

    def creerMenu(self):
        cumulX = 0
        for nom in NOM_ONGLETS:
            frame = tk.Frame(self.menu, background="black")
            button = tk.Menubutton(frame, text=nom, height=HAUTEUR_MENU, font="liberation 20", bg="#CCC", activebackground="#AAA")

            frame.place(height=HAUTEUR_MENU, x=cumulX)
            button.pack(padx=1,pady=1)
            button.update()

            cumulX += button.winfo_width()
            button.bind("<Button-1>", self.creerFonction(nom))
