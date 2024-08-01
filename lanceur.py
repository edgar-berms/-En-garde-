from tkinter import Tk, Frame, Label, Entry, Button, Toplevel, Canvas, Radiobutton
from tkinter.ttk import Label
from PIL import Image, ImageTk
import re

class SimpleDialog(Frame):
    def __init__(self):
        super().__init__()
        self.output1 = ""
        self.output2 = ""
        self.debute1 = False
        self.debute2 = False
        self.couleur = ""
        self.couleur1 = ""
        self.couleur2 = ""
        self.initUI()

    def initUI(self):
        """
        Création de la fenêtre qui permet de rentrer les informations des deux joueurs(nom, couleur des pions, qui commence).
        """
        self.master.title("Initialiser partie")
        self.pack(fill="both", expand=True)

        frame1 = Frame(self)
        frame1.pack(fill="x")

        lbl1 = Label(frame1, text="Joueur 1", width=6)
        lbl1.pack(side="left", padx=5, pady=10)

        self.entry1 = Entry(frame1, textvariable=self.output1)
        self.entry1.pack(fill="x", padx=5, expand=True)

        icone1 = ImageTk.PhotoImage(Image.open("icone_couleur.png").resize((20, 20), Image.LANCZOS))

        btn_couleur1 = Button(frame1, image=icone1, command=lambda: self.toplvl(1))
        btn_couleur1.image = icone1
        btn_couleur1.pack(side="left")
        Radiobutton(frame1, text="Débute", value=1, command=lambda: self.set_debute(1)).pack(side="right")

        frame2 = Frame(self)
        frame2.pack(fill="x")

        lbl2 = Label(frame2, text="Joueur 2", width=6)
        lbl2.pack(side="left", padx=5, pady=10)

        self.entry2 = Entry(frame2, textvariable=self.output2)
        self.entry2.pack(fill="x", padx=5, expand=True)

        icone2 = ImageTk.PhotoImage(Image.open("icone_couleur.png").resize((20, 20), Image.LANCZOS))

        btn_couleur2 = Button(frame2, image=icone2, command=lambda: self.toplvl(2))
        btn_couleur2.image = icone2
        btn_couleur2.pack(side="left")
        Radiobutton(frame2, text="Débute", value=2, command=lambda: self.set_debute(2)).pack(side="right")

        frame3 = Frame(self)
        frame3.pack(fill="x")

        btn_valide = Button(frame3, text="Valider", command=self.onSubmit)
        btn_valide.pack(padx=5, pady=10, side="left")

        btn_annule = Button(frame3, text="Annuler", command=self.quit)
        btn_annule.pack(padx=5, pady=10, side="right")

    def set_debute(self, joueur):
        """
        Pour savoir qui commence.
        """
        if joueur == 1:
            self.debute1 = True
        else:
            self.debute2 = True

    def onSubmit(self):
        """
        Récupere les nom des deux joueurs.
        """
        self.output1 = self.entry1.get()
        self.output2 = self.entry2.get()
        self.destroy()

    def toplvl(self, joueur):
        """
        Fenêtre pour choisir la couleur des pions des joueurs.
        """
        self.tplvl = Toplevel(width=260, height=260)
        self.tplvl.title("couleur")
        self.tplvl.resizable(width=False, height=False)
        self.tplvl.lb = Label(self.tplvl, text="")
        self.tplvl.lb.pack(side="top")
        self.tplvl.cv = Canvas(self.tplvl, width=260, height=260)
        self.tplvl.cv.pack()
        self.tplvl.frm = Frame(self.tplvl)
        self.tplvl.frm.pack(side="bottom")
        self.tplvl.frm.btn_ok = Button(self.tplvl.frm, text="Ok", command=lambda: self.msgCouleur(joueur))
        self.tplvl.frm.btn_ok.pack(side="left")
        self.tplvl.frm.btn_annuler = Button(self.tplvl.frm, text="Annuler", command=lambda: self.msgErreur())
        self.tplvl.frm.btn_annuler.pack(side="right")
        self.creer_matrice(5, 5, tl)

    def msgCouleur(self, joueur):
        """
        Ici on récupere le nom des couleurs qu'on associe avec les joueurs et on ferme la fenêtre.
        """
        if joueur == 1:
            self.couleur1 = self.couleur
        elif joueur == 2:
            self.couleur2 = self.couleur
        self.tplvl.destroy()

    def msgErreur(self):
        """
        Si on clique sur annuler, ferme la fenêtre.
        """
        self.tplvl.destroy()

    def onclick(self, nom_couleur):
        """
        Permet d'afficher le nom de la couleur dans ma fenêtre de séléction de couleur.
        """
        self.couleur = nom_couleur
        self.tplvl.lb.config(text=nom_couleur)
        self.tplvl.lb.config(background=nom_couleur)
        if nom_couleur == "black":
            self.tplvl.lb.config(foreground="white")
        else:
            self.tplvl.lb.config(foreground="black")

    def creer_carre(self, x0, y0, x1, y1, c, joueur):
        """
        Créer un carré d'une certaine couleur.
        """
        tag_carre = f"carre_{c}_{joueur}"
        self.tplvl.cv.create_rectangle(x0, y0, x1, y1, fill=c, tags=tag_carre)
        self.tplvl.cv.tag_bind(tag_carre, "<Button-1>", lambda event, nom_couleur=c : self.onclick(nom_couleur))

    def creer_matrice(self, origineX, origineY, l):
        """
        Créer une matrice de carré de couleur différente.
        """
        taille = 5
        largeur_carre = 50

        for i in range(taille):  # Pour chaque ligne
            for j in range(taille):  # Pour chaque colonne
                couleur = l[i * taille + j]  # Calcul de l'indice pour la liste
                x0 = origineX + j * largeur_carre
                y0 = origineY + i * largeur_carre
                x1 = x0 + largeur_carre
                y1 = y0 + largeur_carre

                joueur = 1 if i < taille // 2 else 2
                self.creer_carre(x0, y0, x1, y1, couleur, joueur)


def creer_liste():
    l = []
    f = open("rgb_mod.txt", "r")
    lines = f.readlines()
    for line in lines:
        l.append(line.strip())
    f.close()
    return l

def transforme_liste(l):
    i = 0
    nl = []
    while i < len(l):
        x = l[i].replace(" ", "").replace("\t", "")
        y = re.sub(r'\d', '', x)
        nl.append(y)
        i = i + 1
    return nl

l = creer_liste()
tl = transforme_liste(l)
