import tkinter as tk

from Action import Action
from Kfetier import Kfetier
from Option import Option
from SpeJour import SpeJour
from Visionner import Visionner

from parametre import NOM_ONGLETS

class Corps():
    def __init__(self, window, corps, menu):
        self.window = window
        self.corps = corps
        self.menu = menu
        self.onglet = None

        self.corps.update()
        self.width = self.corps.winfo_width()
        self.height = self.corps.winfo_height()

    def redefinirTaille(self, width, height):
        self.corps.config(width=width, height=height)
        self.corps.update()
        self.width = width
        self.height = height

    def dessinerOnglet(self, ongletActuel):
        if ongletActuel in NOM_ONGLETS:
            self.viderCorps()

        if ongletActuel == "Actions":
            self.dessinerAction()
        elif ongletActuel == "Kfetier":
            self.dessinerKfetier()
        elif ongletActuel == "Visionner":
            self.dessinerVisionner()
        elif ongletActuel == "Specification Jour":
            self.dessinerSpeJour()
        elif ongletActuel == "Options":
            self.dessinerOption()
        else:
            print(f"l'onglet {ongletActuel} n'est pas correct")
    
    def detruire(self, widget):
        return lambda: widget.destroy()

    def viderCorps(self):
        for widget in self.corps.winfo_children():
            widget.place_forget()
            self.corps.master.after(3000,self.detruire(widget))

    def dessinerAction(self):
        self.onglet = Action(self.corps)

    def dessinerKfetier(self):
        self.onglet = Kfetier(self.window, self.corps)

    def dessinerVisionner(self):
        self.onglet = Visionner(self.corps)

    def dessinerSpeJour(self):
        self.onglet = SpeJour(self.corps)

    def dessinerOption(self):
        self.onglet = Option(self.corps)