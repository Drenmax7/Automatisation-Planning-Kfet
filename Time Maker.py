#application créée par COULON Maxendre, Secretaire de la kfet 2024
#usage, partage et modification libre de l'application tant que mon nom reste credité
#18/05/24


#probleme performence : peut etre les classes des onglets qui ne sont jamais supprimé ou alors les elements des onglets qui ne le sont pas (seconde option surement)
import tkinter as tk
from Menu import Menu
from Corps import Corps

from parametre import HAUTEUR_MENU

class Fenetre():
    def __init__(self, width, height) -> None:
        self.root = tk.Tk()
        self.root.title("Time Maker")

        self.width = width
        self.height = height
        
        self.aChangement = False
        
        self.x = int(self.root.winfo_screenwidth()/2 - self.width/2)
        self.y = int(self.root.winfo_screenheight()/2 - self.height/2)

        self.appliquerTaille()
        self.creerFrame()
        self.menu.creerMenu()
        self.corps.dessinerOnglet(self.menu.ongletActuel)

        self.root.bind("<Configure>", lambda _: self.setChange())
        self.root.bind("<Enter>", lambda _: self.redefinirTaille())

        self.root.mainloop()
    
    def appliquerTaille(self):
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

    def setChange(self):
        if self.width != self.root.winfo_width() or self.height != self.root.winfo_height():
            self.aChangement = True

    def redefinirTaille(self):
        self.x = self.root.winfo_x()
        self.y = self.root.winfo_y()
        if self.aChangement:
            self.aChangement = False
            
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()

            self.menu.redefinirTaille(self.width)
            self.corps.redefinirTaille(self.width, self.height-HAUTEUR_MENU)
            
            self.corps.dessinerOnglet(self.menu.ongletActuel)

    def creerFrame(self):
        menuFrame = tk.Frame(self.root,width=self.width, height=HAUTEUR_MENU)
        menuFrame.grid(row=0)
        self.menu = Menu(menuFrame)
        
        corpsFrame = tk.Frame(self.root, bg="#DDD", width=self.width, height=self.height-HAUTEUR_MENU)
        corpsFrame.grid(row=1)
        self.corps = Corps(self.root, corpsFrame, self.menu)

        self.menu.corps = self.corps



root = Fenetre(960,540)


