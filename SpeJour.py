import tkinter as tk

from fonction import bind_tree
from parametre import SPECIALITE_JOUR, CHEMIN_RESSOURCES, SPECIALITE_GENERAL, NOM_PERIODES, NOM_JOUR, COULEUR_CORPS,ALTERNANCE_COULEUR

#spe jour ->  permet de changer les jours et periode pour lesquels il faut attribuer des gens, les effectifs par periode, effectif generaux (change egalement les effectif specifique)
#

class SpeJour():
    def __init__(self, root) -> None:
        self.root = root

        self.padding = 10
        self.width = self.root.winfo_width() - 2*self.padding
        self.height = self.root.winfo_height() - 2*self.padding

        self.listeCheckbox = {}
        self.spinbox = {}
        self.var = []
        
        self.speJour = self.lire(CHEMIN_RESSOURCES+SPECIALITE_JOUR)
        self.speGen = self.lire(CHEMIN_RESSOURCES+SPECIALITE_GENERAL)

        self.dessinerGrille()

        self.enregistre(CHEMIN_RESSOURCES+SPECIALITE_JOUR, self.speJour)
        self.enregistre(CHEMIN_RESSOURCES+SPECIALITE_GENERAL, self.speGen)
    
    @staticmethod
    def lire(nom):
        fichier = open(nom, "r", encoding="UTF-8")
        data = fichier.read()
        fichier.close()
        return eval(data)

    @staticmethod
    def enregistre(nom, data):
        fichier = open(nom, "w", encoding="UTF-8")
        fichier.write(str(data))
        fichier.close()
    
    def placerParametre(self, contenu):        

        backConfig = tk.Frame(contenu, bg="black")
        backConfig.place(x=self.width,anchor="ne",height=self.height)
        config = tk.Frame(backConfig, bg=COULEUR_CORPS)
        config.pack(padx=2,pady=2,fill="y",expand=True)
        self.config = backConfig
        
        titre = tk.Frame(config)
        titre.grid(row=0, pady=(0,5))
        label = tk.Label(titre, text="Effectifs", font="liberation 17", bg=COULEUR_CORPS)
        label.pack()

        for i in range(len(NOM_PERIODES)):
            periode = NOM_PERIODES[i]
            param = tk.Frame(config)
            param.grid(row=i+1,sticky="e", pady=(0,5))

            var = tk.StringVar(param)
            var.set(self.speGen[periode])
            entry = tk.Spinbox(param, font="liberation 15",width=3, from_=1, to=99, textvariable=var)
            entry.pack(side="right")

            var.trace_add("write", callback=lambda *_, var=var, periode=periode:self.changerSpeGen(periode, var.get()))
            self.var.append(var)

            label = tk.Label(param, text=f"{periode} : ", font="liberation 15", bg=COULEUR_CORPS)
            label.pack(side="right", expand=True)
        
        backConfig.update()

    def placerJour(self, frame, nom):
        self.spinbox[nom] = []
        numJour = NOM_JOUR.index(nom)

        backJour = tk.Frame(frame, bg="black")
        backJour.place(x=0, width=frame.winfo_width()//7*3, height=frame.winfo_height())
        jour = tk.Frame(backJour,bg=ALTERNANCE_COULEUR[1][(numJour)%2])
        jour.pack(padx=(0,2),fill="both",expand=True)

        var = tk.IntVar()
        checkbox = tk.Checkbutton(jour,bg=ALTERNANCE_COULEUR[1][(numJour)%2], text=nom, font="liberation 20", 
                                  variable=var, command=lambda nomJour=nom, state=var:self.toggleJour(nomJour, state),
                                  activebackground = ALTERNANCE_COULEUR[1][(numJour)%2])
        checkbox.pack(expand=True, fill="both")
        
        if self.speGen["Jours"][numJour] == 1:
            checkbox.select()
        self.listeCheckbox[nom]= {"" : checkbox}

        heightLeft = frame.winfo_height()
        for i in range(len(NOM_PERIODES)):
            nomPeriode = NOM_PERIODES[i]
            effectif = self.speJour[nom][nomPeriode]

            height = heightLeft// (len(NOM_PERIODES)-i)
            x = frame.winfo_width()//7*3
            y = frame.winfo_height() - heightLeft
            heightLeft -= height
            backButton = tk.Frame(frame,bg="black")
            backButton.place(x=x, y=y, width=frame.winfo_width()//7*3, height=height)
            
            var = tk.IntVar()
            button = tk.Checkbutton(backButton, bg=ALTERNANCE_COULEUR[0][(numJour+i)%2], text=nomPeriode, font="liberation 15", 
                                    variable=var, activebackground=ALTERNANCE_COULEUR[0][(numJour+i)%2], 
                                    command=lambda state=var, i=i:self.togglePeriode(i+3*numJour, state))
            button.pack(fill="both",expand=True,padx=(0,1),pady=(0,1 if i < len(NOM_PERIODES)-1 else 0))
            if effectif != 0:
                button.select()
            self.listeCheckbox[nom][nomPeriode] = button
            
            backEntry = tk.Frame(frame, bg="black")
            backEntry.place(x=frame.winfo_width()//7*6, y=y, width=frame.winfo_width()//7*1, height=height)

            entryFrame = tk.Frame(backEntry, bg=ALTERNANCE_COULEUR[0][(numJour+i)%2])
            entryFrame.pack(fill="both",expand=True,pady=(0,1 if i < len(NOM_PERIODES)-1 else 0))
            var = tk.IntVar()
            var.set(effectif)
            entry = tk.Spinbox(entryFrame, font="liberation 15",from_=0, to=99, textvariable=var, bg=ALTERNANCE_COULEUR[0][(numJour+i)%2])
            entry.pack(fill="both",expand=True)

            var.trace_add("write", callback=lambda *_, nomPeriode=nomPeriode,var=var:self.changerSpeJour(nom,nomPeriode,var))
            self.var.append(var)

            self.spinbox[nom].append(entry)

    def changerSpeJour(self, jour, periode, var):
        try: #si le contenu est vidé ca pose probleme
            valeur = var.get()
            self.speJour[jour][periode] = valeur
            self.enregistre(CHEMIN_RESSOURCES+SPECIALITE_JOUR, self.speJour)

            checkbox = self.listeCheckbox[jour][periode]
            if valeur == 0:
                checkbox.deselect()
            else:
                checkbox.select()

        except tk.TclError:
            pass

    def changerSpeGen(self, periode, value):
        self.speGen[periode] = value
        numPeriode = NOM_PERIODES.index(periode)

        for jour in self.spinbox:
            spinbox = self.spinbox[jour][numPeriode]
            if spinbox.get() != "0":
                spinbox.delete(0,tk.END)
                spinbox.insert(0,value)

        self.enregistre(CHEMIN_RESSOURCES+SPECIALITE_GENERAL, self.speGen)

    def togglePeriode(self, numPeriode, state):
        nomJour = NOM_JOUR[numPeriode//3]
        nomPeriode = NOM_PERIODES[numPeriode%3]
        spinbox = self.spinbox[nomJour][numPeriode%3]
        value = self.speGen[nomPeriode] if state.get() else 0
        self.speJour[nomJour][nomPeriode] = value

        spinbox.delete(0,tk.END)
        spinbox.insert(0,value)

    def toggleJour(self, nomJour, state):
        numJour = NOM_JOUR.index(nomJour)
        self.speGen["Jours"][numJour] = state.get()
        self.enregistre(CHEMIN_RESSOURCES+SPECIALITE_GENERAL, self.speGen)

        for i in range(len(self.spinbox[nomJour])):
            nomPeriode = NOM_PERIODES[i]
            spinbox = self.spinbox[nomJour][i]
            value = self.speGen[nomPeriode] if state.get() else 0
            self.speJour[nomJour][nomPeriode] = value

            spinbox.delete(0,tk.END)
            spinbox.insert(0,value)
        
        self.enregistre(CHEMIN_RESSOURCES+SPECIALITE_JOUR, self.speJour)

    def placerContenu(self, contenu):
        backSemaine = tk.Frame(contenu, bg="black")
        backSemaine.place(x=0,height=self.height, width=self.width-self.config.winfo_width())
        semaine = tk.Frame(backSemaine, bg=COULEUR_CORPS)
        semaine.pack(padx=(2,0),pady=2,fill="both",expand=True)

        semaine.update()

        heightLeft = semaine.winfo_height()
        for i in range(len(NOM_JOUR)):
            nom = NOM_JOUR[i]

            backJour = tk.Frame(semaine, bg="black", width=100,height=50)
            y = semaine.winfo_height() - heightLeft
            height = heightLeft//(len(NOM_JOUR)-i)
            heightLeft -= height
            backJour.place(y=y, height=height, width=semaine.winfo_width())

            jour = tk.Frame(backJour, bg=COULEUR_CORPS)
            jour.pack(pady=(0,2 if i < len(NOM_JOUR)-1 else 0),fill="both",expand=True)

            jour.update()
            self.placerJour(jour, nom)

    def dessinerGrille(self):
        contenu = tk.Frame(self.root, width=self.width, height=self.height)
        contenu.place(x=self.padding,y=self.padding)

        self.placerParametre(contenu)
        self.placerContenu(contenu)



        






