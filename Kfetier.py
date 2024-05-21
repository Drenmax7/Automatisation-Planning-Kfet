import tkinter as tk

from parametre import COORDONNEES_MEMBRE, CHEMIN_RESSOURCES, BASE_DELTA_VALUE, FORCE_SCROLL, FORCE_FLECHE, ALTERNANCE_COULEUR, COULEUR_CORPS
from fonction import bind_tree

#kfetier ->   tableau montrant tout les kfetier, permet la modification de leurs informations, d'en rajouter, d'en supprimer
#             genere le exel permettant de demander les dispo lors de la sauvegarde
#commandes : deplacer commande, trié les lignes en fonction d'une colonne, scroll avec la molette, shift molette, les 4 fleches, double click sur case pour la modifier, 
#entrée ou click sur une autre case pour confirmer, ajouter case avec le +, supprimer en vidant le contenu de la case de la colonne nom prenom
class Kfetier():
    def __init__(self, window, root) -> None:
        self.window = window
        self.root = root
        self.fichier = CHEMIN_RESSOURCES+COORDONNEES_MEMBRE

        self.decalageX = 0
        self.decalageY = 0
        self.ordre = ""
        self.entry = None
        self.tableau = None
        self.nePasDetruire = False
        
        self.padding = 10
        self.tableWidth = self.root.winfo_width() - self.padding*2 - 50
        self.tableHeight = self.root.winfo_height() - self.padding*2

        self.lire(self.fichier)


        self.dessinerTableau()
        
        self.bindArrow()
    
    def bindArrow(self):
        self.window.bind("<Left>", lambda _:self.changerX(-1 * FORCE_FLECHE * FORCE_SCROLL))
        self.window.bind("<Right>", lambda _:self.changerX(FORCE_FLECHE * FORCE_SCROLL))
        self.window.bind("<Up>", lambda _:self.changerY(-1 * FORCE_FLECHE * FORCE_SCROLL))
        self.window.bind("<Down>", lambda _:self.changerY(FORCE_FLECHE * FORCE_SCROLL))

    def unbindArrow(self):
        self.window.bind("<Left>", lambda _:None)
        self.window.bind("<Right>", lambda _:None)
        self.window.bind("<Up>", lambda _:None)
        self.window.bind("<Down>", lambda _:None)

    def determineMolette(self, event):
        #valeur impair si il s'agit d'une molette horizontal
        if event.state%2:
            self.changerX(-event.delta//BASE_DELTA_VALUE * FORCE_SCROLL)
        else:
            self.changerY(-event.delta//BASE_DELTA_VALUE * FORCE_SCROLL)

    def changerX(self, valeur):
        largeurColonne = self.listeColonne[-1][0].winfo_width() + self.listeColonne[-1][1] + len(self.listeLigne)
        largeurTableau = self.tableau.winfo_width()
        upLimit = largeurColonne - largeurTableau

        if 0 <= self.decalageX <= upLimit:
            self.decalageX = max(min(self.decalageX+valeur,upLimit),0)
            self.rechargerTableau()

    def changerY(self, valeur):
        hauteurColonne = self.listeColonne[0][0].winfo_height()
        hauteurTableau = self.tableau.winfo_height()
        upLimit = hauteurColonne - hauteurTableau + len(self.info)+2

        if 0 <= self.decalageY <= upLimit:
            self.decalageY = max(min(self.decalageY+valeur,upLimit),0)
            self.rechargerTableau()

    def rechargerTableau(self):
        for widget in self.listeColonne+self.listeLigne:
            colonne,originalX = widget
            colonne.place(x=originalX-self.decalageX, y=-self.decalageY)


    def lire(self, fichier):
        f = open(fichier, "r", encoding="UTF-8")
        data = [i.split(";") for i in f.read().split("\n") if i != ""]
        f.close()

        self.colonne = data[0]
        self.info = data[1:]
    
    def enregistre(self, fichier):
        f = open(fichier, "w", encoding="UTF-8")
        
        texte = ",".join(self.colonne)+"\n"
        f.write(texte.replace(",",";"))
        
        for ligne in self.info:
            texte = ",".join(ligne)+"\n"
            f.write(texte.replace(",",";"))

        f.close()
    
    def deplaceColonne(self, emplacementDebut, emplacementFin):
        col = self.colonne[emplacementDebut]
        del self.colonne[emplacementDebut]
        self.colonne.insert(emplacementFin, col)

        for ligne in self.info:
            colInfo = ligne[emplacementDebut]
            del ligne[emplacementDebut]
            ligne.insert(emplacementFin, colInfo)
        self.enregistre(self.fichier)

        self.tableau.destroy()
        self.dessinerTableau()
        
    def deplacerLigne(self, emplacementDebut, emplacementFin):
        ligne = self.info[emplacementDebut]
        del self.info[emplacementDebut]
        self.info.insert(emplacementFin, ligne)

    def trier(self, nom, croissant=True):
        self.ordre = nom if croissant else ""

        num = self.colonne.index(nom)
        self.info.sort(key=lambda x: x[num], reverse= not(croissant))
        self.enregistre(self.fichier)

        self.tableau.destroy()
        self.dessinerTableau()

    def relache(self, event):
        if 0 <= event.y < event.widget.winfo_height():
            nomCol = event.widget.cget("text")

            if 0 <= event.x < event.widget.winfo_width():
                self.trier(nomCol, croissant=self.ordre != nomCol)

            else:
                num = self.colonne.index(nomCol)
                tabX = event.x + self.listeColonne[num][1]
                largeurColonne = self.listeColonne[-1][0].winfo_width() + self.listeColonne[-1][1] + len(self.listeLigne)
                if 0 <= tabX < largeurColonne:
                    for i in range(len(self.listeColonne)):
                        if tabX >= self.listeColonne[i][1]:
                            numArrive = i
                    self.deplaceColonne(num, numArrive)
    
    def ajouterLigne(self):
        ligne = []
        for nomCol in self.colonne:
            if nomCol == "Prenom Nom":
                ligne.append("Nouvelle Personne")
            else:
                ligne.append("")

        self.info.insert(0,ligne)
        self.tableau.destroy()
        self.dessinerTableau()

    def doubleClick(self, event):
        if self.entry != None:
            self.confirmer()

        self.label = event.widget
        master = event.widget.master

        text = self.label.cget("text")
        font = self.label.cget("font")
        bg = self.label.cget("bg")
        width = self.label.winfo_width()

        self.entry = tk.Entry(master, font=font, bg=bg, justify=tk.CENTER)
        self.entry.insert(tk.END, text)
        self.entry.place(x=0, width=width)
        self.entry.focus_set()

        self.unbindArrow()
        
        self.entry.bind("<Return>", lambda _: self.confirmer())
    
    def confirmer(self):
        if self.entry != None:
            entry = self.entry
            self.entry = None

            texte = entry.get()
            entry.place_forget()

            self.label.config(text=texte)
            numCol,numCase = self.label.emplacement
            
            self.info[numCase][numCol] = texte
            self.bindArrow()
            
            if texte == "" and self.colonne[numCol] == "Prenom Nom":
                del self.info[numCase]
                self.enregistre(self.fichier)
                self.tableau.destroy()
                self.dessinerTableau()
            else:
                self.enregistre(self.fichier)
            
        
    def boutonAjout(self):
        bouton = tk.Button(self.bigFrame, text="+", font="liberation 20", border=6, command=self.ajouterLigne)
        bouton.place(x=self.tableau.winfo_width() + 2*self.padding, y=self.padding, width=40, height=40)

    def dessinerTableau(self):

        self.bigFrame = tk.Frame(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), bg=COULEUR_CORPS)
        self.bigFrame.place(x=0)

        padding = self.padding
        width = self.tableWidth
        height = self.tableHeight

        if self.tableau != None:
            self.tableau.destroy()
        self.tableau = tk.Frame(self.bigFrame, width=width, height=height, bg=COULEUR_CORPS)
        self.tableau.place(x=padding,y=padding)

        cumulX = 1
        self.listeColonne = []
        self.listeLigne = []
        for numCol in range(len(self.colonne)):
            colonne = tk.Frame(self.tableau, bg="black")
            colonne.place(x=cumulX-self.decalageX, y=-self.decalageY)
            self.listeColonne.append((colonne,cumulX))

            nomCol = self.colonne[numCol]
            caseT = tk.Frame(colonne)
            caseT.pack(fill="x", pady=(1,1))

            label = tk.Label(caseT, text=nomCol, font="liberation 15", bg=ALTERNANCE_COULEUR[0][0], )
            label.pack(fill="x")
            label.bind("<ButtonRelease-1>", lambda event: self.relache(event))

            for numCase in range(len(self.info)):
                ligne = self.info[numCase]
                color = ALTERNANCE_COULEUR[0][0] if numCase%2 else ALTERNANCE_COULEUR[0][1]

                caseT = tk.Frame(colonne)
                caseT.pack(fill="x", pady=(0,1))
                
                infoCase = ligne[numCol]
                label = tk.Label(caseT, text=infoCase, font="liberation 15", bg=color)
                label.emplacement = (numCol,numCase)
                label.pack(fill="x")

                label.bind("<Double-Button-1>",lambda event:self.doubleClick(event))
                label.bind("<Button-1>",lambda _:self.confirmer())
            
            colonne.update()
            cumulX += colonne.winfo_width()

        x = cumulX
        for i in range(len(self.listeColonne)+1):
            ligne = tk.Frame(self.tableau, width=1, height=colonne.winfo_height(), bg="black")
            ligne.place(x=x-self.decalageX, y=-self.decalageY)
            self.listeLigne.append((ligne,x))

            x = self.listeColonne[i][1] if i<len(self.listeColonne) else None
        
        largeurColonne = self.listeColonne[-1][0].winfo_width() + self.listeColonne[-1][1] + len(self.listeLigne)
        self.tableau.configure(width=min(self.tableWidth,largeurColonne))
        self.tableau.update()       
        
        bind_tree(self.root, "<MouseWheel>", lambda event: self.determineMolette(event))
        
        self.boutonAjout()

