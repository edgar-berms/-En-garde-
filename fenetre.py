from tkinter import messagebox
from tkinter import font
import tkinter as tk
from PIL import Image, ImageTk
from lanceur import *
from joueur import Joueur
from deck import Deck
import random

class Fenetre(tk.Tk):
    # Ajoutez une variable de classe pour stocker les cases
    cases = []

    def __init__(self):
        super().__init__()

        self.title("En garde !")

        bold_font = font.Font(weight="bold")
        self.lb = tk.Label(self, text=" {} // {} ".format(10, 10), relief="solid", borderwidth=5, font=bold_font,justify="center")
        self.lb.pack(side="top")
        self.lb_deck = tk.Label(self, text="Carte restante dans le deck : {}".format(25),font=bold_font,justify="center")
        self.lb_deck.pack(side="top")

        self.cv = tk.Canvas(self)
        self.cv.pack(fill=tk.BOTH, expand=True)
        
        self.cv_im = tk.Canvas(self)
        self.cv_im.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.cv_im.pack_forget()
        
        self.cv_bouton = tk.Canvas(self)
        self.cv_bouton.pack()

        self.cv.cols = 23

        # Créez les cases initiales
        self.create_cases()

        self.bind("<Configure>", self.on_canvas_resize)

        self.joueur1 = Joueur("j1","white")
        self.joueur2 = Joueur("j2","white")
        self.deck = None
        
        #########################################################
        self.joueur_actuel = None
        self.manche = 0.5
        #########################################################

        self.bouton_jouer = tk.Button(self.cv_bouton, text="Jouer", command=self.initialiser_partie)
        self.bouton_jouer.pack()
        self.bouton_regle = tk.Button(self.cv_bouton, text="Règle", command=self.regle)
        self.bouton_regle.pack()
        
        self.indice_carte_joue = None
        self.defendre = False
        self.a = 0
        
        self.confettis = []
        
    def regle(self):
        """
        Créatoin d'une fenêtre qui affiche les règles.
        """
        self.rule = tk.Toplevel(self)
        self.rule.title("Règle")
        self.rule.resizable(width=False, height=False)
        
        texte_initiale = self.charger_texte()

        self.rule_text = tk.Text(self.rule, wrap=tk.WORD, state=tk.NORMAL)
        self.rule_text.insert(tk.END,texte_initiale)
        self.rule_text.config(state=tk.DISABLED)
        self.rule_text.pack(padx=20, pady=20)

        # Ajouter un bouton pour fermer la fenêtre
        bouton_ok = tk.Button(self.rule, text="Ok", command=self.fermer_regle)
        bouton_ok.pack()

    def fermer_regle(self):
        """
        Fonction pour fermer la fenêtre des règles du jeu.
        """
        self.rule_text.destroy()
        self.rule.destroy()

    def charger_texte(self):
        """
        Fonction qui permet de lire un fichier .txt qui contient les règles pour l'afficher dans ma fenêtre. Aidé par chatgpt.
        """
        try:
            with open("texte_regle.txt", "r") as fichier:
                return fichier.read()
        except FileNotFoundError:
            return ""

    # Initialisez la liste des cases une seule fois
    def create_cases(self):
        """
        Créer les cases qui correspondent à notre plateau de jeu.
        """
        if not Fenetre.cases:
            cell_width = self.winfo_width() // self.cv.cols
            for col in range(self.cv.cols):
                x1 = (col * cell_width) + 5
                y1 = 50
                x2 = x1 + cell_width
                y2 = y1 + 100
                case = self.cv.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
                Fenetre.cases.append(case)
                
    def delete_cases(self):
        """
        Supprime les cases qui correspondent à notre plateau de jeu.
        """
        for case in Fenetre.cases:
            self.cv.delete(case)

        Fenetre.cases = []
            
    def afficher_image(self):
        """
        Affiche les png des cartes qui sont dans la main du joueur actuel.
        """
        self.photo_list = []
        for carte in self.carte_photo():
            image = Image.open(carte)
            resized_image = image.resize((75, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            self.photo_list.append(photo)

        self.cv_im.delete("carte_image")

        for i, photo in enumerate(self.photo_list):
            tag = f"carte_image_{i}"
            self.cv_im.create_image(i * 75 + 40, 100, anchor=tk.N, image=photo, tags=("carte_image",tag))
            self.cv_im.tag_bind(tag,"<Button-1>",lambda event,index = i : self.image_cliquee(index))
            
    def image_cliquee(self,index):
        """
        Fonction qui mets à jour self.indice_carte_joue grâce au clique de l'utilisateur sur une carte et entoure la carte cliqué par un liseret rouge.
        On appelle aussi déplacement pour afficher les boutons qui permette de générer les déplacmeents possible.
        """
        self.indice_carte_joue = index
        self.cv_im.delete("carte_rectangle")
        x0 = index * 75
        y0 = 100
        x1 = x0 + 75
        y1 = y0 + 100
        self.cv_im.create_rectangle(x0, y0, x1, y1, outline="red", width=5, tags="carte_rectangle")
        if(self.defendre == False):
            self.deplacement(self.indice_carte_joue)
        else:
            self.defenseur()

    def on_canvas_resize(self, event):
        """
        Méthode pour réapeller et réafficher les canvas lors d'un redimensinnage de fenêtre. Généré par chatGpt. 
        """
        if self.cv.winfo_exists():
            Fenetre.cases = []
            self.create_cases()
            self.maj_plateau()
            
    def changer_couleur_case(self, col, couleur):
        """
        Change la couleur de la case de la colonne donné.
        """
        case = Fenetre.cases[col]
        self.cv.itemconfig(case, fill=couleur)

    def initialiser_partie(self):
        """
        Ensemble d'instruction pour initialiser la partie avec les bons paramètres.
        """
        self.bouton_jouer.pack_forget()
        self.bouton_regle.pack_forget()
        
        app = SimpleDialog()
        
        # Utilisez wait_window pour bloquer l'exécution jusqu'à ce que la fenêtre soit fermée
        self.wait_window(app)

        self.joueur1.set_nom = app.output1
        self.joueur2.set_nom = app.output2
        self.joueur1.set_couleur = app.couleur2
        self.joueur2.set_couleur = app.couleur1
        if app.debute1 == True:
            commence = self.joueur1
        elif app.debute2 == True:
            commence = self.joueur2
        else:
            print("erreur")
            
        self.deck = Deck()
        
        self.bouton_gauche = tk.Button(self.cv_bouton,text="Gauche",command=lambda : self.deplacement_gauche())
        self.bouton_gauche.pack(side="left")
        self.bouton_gauche.pack_forget()
        self.bouton_droite = tk.Button(self.cv_bouton,text="Droite",command=lambda : self.deplacement_droite())
        self.bouton_droite.pack(side="right")
        self.bouton_droite.pack_forget()
        self.bouton_attaque = tk.Button(self.cv_bouton,text="Attaque",command=lambda : self.attaque())
        self.bouton_attaque.pack()
        self.bouton_attaque.pack_forget()
        self.bouton_defense = tk.Button(self.cv_bouton,text="Défense",command=lambda : self.defense())
        self.bouton_defense.pack()
        self.bouton_defense.pack_forget()
        self.cv_im.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.maj_plateau()
        self.demarrer_partie(commence)
        self.maj_plateau()


    def maj_plateau(self):
        """
        Ensemble de méthode qui permette de mettre à jour l'interface (position des joueurs, mains et score).
        """
        self.changer_couleur_case(self.joueur1.get_temp,"white")
        self.changer_couleur_case(self.joueur2.get_temp,"white")
        self.changer_couleur_case(self.joueur1.get_position + len(Fenetre.cases)-1 - 22, self.joueur1.get_couleur)
        self.changer_couleur_case(self.joueur2.get_position + len(Fenetre.cases)-1 - 22, self.joueur2.get_couleur)
        

        self.lb.config(text=" {} // {} ".format(self.joueur2.get_score, self.joueur1.get_score))
        if(self.deck is not None):
            self.lb_deck.config(text="Carte restante dans le deck : {}".format(self.deck.nb_carte_restant()))
        
        if self.manche >= 1 and self.defendre == False:
            self.afficher_image()
        
    def launch(self):
        """
        Fonction pour créer la boucle principale.
        """
        self.mainloop()
        
    def demarrer_partie(self,commence):
        """
        Liste d'instruction afin de démarrer une partie de notre jeu.
        """
        self.bouton_droite.pack_forget()
        self.bouton_gauche.pack_forget()
        self.deck.remplir()
        self.deck.melange()
        self.joueur1.set_position = 0
        self.joueur2.set_position = 22
        self.joueur_actuel = commence
        self.debut()
        self.manche_suivante()
        
    def manche_suivante(self):
        """
        Fonction principale qui compte le nombre de manche, à qui est le tour et si il y a un gagnant !!
        """
        self.cv_im.pack_forget()
        
        # Vérifier s'il y a un gagnant
        if self.joueur1.get_score == 5 or self.joueur2.get_score == 5:
            self.fin_partie()
            
        self.manche += 0.5
        self.bouton_droite.pack_forget()
        self.bouton_gauche.pack_forget()
        messagebox.showinfo("Info", f"\nManche {int(self.manche)}\n\n Joueur qui joue {self.joueur_actuel.get_nom}")
        self.cv_im.pack()

        # Passer au joueur suivant
        self.change_joueur()
        
    def change_joueur(self):
        """
        Fonction pour changer le joueur actuel, c'est à dire le joueur qui doit jouer.
        """
        if self.joueur_actuel == self.joueur1:
            self.joueur_actuel = self.joueur2
        elif self.joueur_actuel == self.joueur2:
            self.joueur_actuel = self.joueur1
        
    def attaque(self):
        """
        Fonction qui permet de lancer une attaque.
        """
        self.defendre = True
        self.joueur_actuel.sup_main(self.indice_carte_joue)
        self.piocher(self.joueur_actuel)
        self.bouton_attaque.pack_forget()
        self.cv_im.pack_forget()
        messagebox.showinfo("Info", f"\nManche {int(self.manche)}\n\n Joueur qui joue {self.joueur_actuel.get_nom}")
        self.change_joueur()
        self.cv_im.pack()
        self.afficher_image()
        
    def defenseur(self):
        """
        Fonction qui permet d'afficher le bouton défense.
        """
        self.bouton_defense.pack()
        
    def defense(self):
        """
        Fonction qui permet au joueur qui doit se défendre de choisir une carte et de la jouer.
        Si la carte est de même valeur que celle qui a permis l'attaque alors il survit et le jeu continu mais sinon il perd la manche.
        """
        carte = self.joueur_actuel.get_carte_main(self.indice_carte_joue)
        step = carte.get_num
        
        if (self.a != step):
             self.fin_manche()
        else:        
            self.joueur_actuel.sup_main(self.indice_carte_joue)
            self.piocher(self.joueur_actuel)   
            self.indice_carte_joue = None
            self.manche_suivante()
        
        self.defendre = False
        self.a = 0
        self.maj_plateau()
        self.bouton_defense.pack_forget()
    
    def fin_partie(self):
        """
        Affiche le gagnant(c'est à dire le premier à 5 points) et quitte l'application.
        """
        self.cv.unbind("<Configure>")
        self.cv_im.destroy()
        self.cv_bouton.destroy()
        self.cv.destroy()
        self.lb.destroy()
        self.lb_deck.destroy()
        self.cv_conf = tk.Canvas(self,bg = "black")
        self.cv_conf.pack()
        self.lancer_confettis()
        messagebox.showinfo("Victoire",f"\nLe joueur {self.joueur_actuel.get_nom} a remporté la partie!")
        exit()
    
    def fin_manche(self):
        """
        Fonction appelé à la fin d'une manche.
        Elle s'occupe d'augmenter le score du gagnant et de réinitialiser les mains, le deck et le plateau ainsi que relancer une partie vierge.
        """
        self.manche = 0.5
        self.joueur_actuel.score_plus_un()
        messagebox.showinfo("Gagnant manche", f"{self.joueur_actuel.get_nom} a remporté la manche!")
        self.joueur1.vide_main()
        self.joueur2.vide_main()
        self.deck.vide_deck()
        self.delete_cases()
        self.create_cases()
        self.change_joueur()
        self.demarrer_partie(self.joueur_actuel)
        
    def debut(self):
        """
        Distribution des cartes pour les deux joueurs.
        """
        for i in range(5):
            self.piocher(self.joueur1)
            self.piocher(self.joueur2)
            
    def carte_photo(self):
        """
        A partir de la main du joueur actuel, on crée une liste de chaine de caractère qui correspondent aux noms des images des cartes au format png.
        """
        l = []
        for carte in self.joueur_actuel.get_main:
            l.append(f"carte_{carte.get_num}.png")
        return l

    def piocher(self, j):
        """
        Fonction pour piocher une carte.
        """
        if not self.deck.est_vide():
            if(self.joueur2.get_position < 22 - self.joueur1.get_position):
                self.joueur_actuel = self.joueur1
                self.fin_manche()
            else:
                self.joueur_actuel = self.joueur2
                self.fin_manche()
        else:
            carte_sommet = self.deck.retirer_carte()
            j.ajout_main(carte_sommet)
            
    def lancer_confettis(self):
        for _ in range(10):  # Nombre de confettis
            x = random.randint(50, 750)
            y = 0
            couleur = random.choice(["peach puff","lavender","black","grey","slate blue","blue","light blue","turquoise","cyan","dark olive green","green","chartreuse","yellow","gold","tan","brown","salmon","orange","coral","red","pink","maroon","magenta","orchid","purple"])
            confetti = self.creer_confetti(x, y, couleur)
            self.confettis.append(confetti)

        self.deplacer_confettis()
        self.after(100, self.lancer_confettis)  # Répéter toutes les secondes

    def creer_confetti(self, x, y, couleur):
        taille = random.randint(5, 15)
        confetti = self.cv_conf.create_rectangle(x, y, x+taille, y+taille, fill=couleur, outline="")
        return confetti

    def deplacer_confettis(self):
        for confetti in self.confettis:
            coords = self.cv_conf.coords(confetti)
            if coords and coords[1] < 600:  # Vérifier si les coordonnées ne sont pas vides et le confetti n'a pas atteint le bas de la fenêtre
                dx = random.uniform(-1, 1)
                dy = random.uniform(0.25, 1)  # Ajuster cette valeur pour ralentir la vitesse de descente
                self.cv_conf.move(confetti, dx, dy)
            else:
                self.cv_conf.delete(confetti)  # Supprimer le confetti une fois en bas

        self.update()
        self.after(30, self.deplacer_confettis)  # Délai entre les images

    def deplacement(self, indice):
        """
        Fonction qui permet d'afficher les boutons des déplacements disponibles pour le joueur actuel.
        """
        self.bouton_droite.pack_forget()
        self.bouton_gauche.pack_forget()
        self.bouton_attaque.pack_forget()
        if indice is not None:
            carte = self.joueur_actuel.get_carte_main(indice)
            self.joueur_actuel.set_temp = self.joueur_actuel.get_position
            step = carte.get_num
            if (self.joueur_actuel == self.joueur1):
                if (self.joueur_actuel.get_position + step < self.joueur2.get_position and self.joueur_actuel.get_position - step > 0):
                    self.bouton_gauche.pack(side="left")
                    self.bouton_droite.pack(side="right")
                elif (self.joueur_actuel.get_position + step == self.joueur2.get_position):
                    self.a = step
                    self.bouton_attaque.pack()
                elif (self.joueur_actuel.get_position + step < self.joueur2.get_position):
                    self.bouton_droite.pack(side="right")
                elif (self.joueur_actuel.get_position - step > 0):
                    self.bouton_gauche.pack(side="left")
            else:
                if (self.joueur_actuel.get_position + step < 23 and self.joueur_actuel.get_position - step > self.joueur1.get_position):
                    self.bouton_gauche.pack(side="left")
                    self.bouton_droite.pack(side="right")
                elif (self.joueur_actuel.get_position - step == self.joueur1.get_position):
                    self.a = step
                    self.bouton_attaque.pack()
                elif (self.joueur_actuel.get_position + step < 23):
                    self.bouton_droite.pack(side="right")
                elif (self.joueur_actuel.get_position - step > self.joueur1.get_position):
                    self.bouton_gauche.pack(side="left")

    
    def deplacement_droite(self):
        """
        Fonction appelé par le bouton droite qui permet d'effectuer le déplacement vers la droite du joueur actuel.
        """
        # Obtenir la carte jouée en fonction de l'indice sauvegardé
        carte = self.joueur_actuel.get_carte_main(self.indice_carte_joue)
        step = carte.get_num
        adversaire = self.joueur1 if self.joueur_actuel == self.joueur2 else self.joueur2

        if (self.joueur_actuel == self.joueur1) and (self.joueur_actuel.get_position + step < adversaire.get_position):
            self.joueur_actuel.set_position = self.joueur_actuel.get_position + step
        elif (self.joueur_actuel == self.joueur2) and (self.joueur_actuel.get_position + step > adversaire.get_position):
            self.joueur_actuel.set_position = self.joueur_actuel.get_position + step

        self.joueur_actuel.sup_main(self.indice_carte_joue)
        self.piocher(self.joueur_actuel)

        # Réinitialiser les variables d'état dans la fenêtre
        self.indice_carte_joue = None

        self.manche_suivante()
        self.maj_plateau()
        self.bouton_droite.pack_forget()
        self.bouton_gauche.pack_forget()
                
        
    def deplacement_gauche(self):
        """
        Fonction appelé par le bouton gauche qui permet d'effectuer le déplacement vers la gauche du joueur actuel.
        """
        # Obtenir la carte jouée en fonction de l'indice sauvegardé
        carte = self.joueur_actuel.get_carte_main(self.indice_carte_joue)
        step = carte.get_num
        adversaire = self.joueur1 if self.joueur_actuel == self.joueur2 else self.joueur2

        if (self.joueur_actuel == self.joueur1) and (self.joueur_actuel.get_position - step < adversaire.get_position):
            self.joueur_actuel.set_position = self.joueur_actuel.get_position - step
        elif (self.joueur_actuel == self.joueur2) and (self.joueur_actuel.get_position - step > adversaire.get_position):
            self.joueur_actuel.set_position = self.joueur_actuel.get_position - step

        self.joueur_actuel.sup_main(self.indice_carte_joue)
        self.piocher(self.joueur_actuel)

        # Réinitialiser les variables d'état dans la fenêtre
        self.indice_carte_joue = None
        
        self.manche_suivante()
        self.maj_plateau()
        self.bouton_droite.pack_forget()
        self.bouton_gauche.pack_forget()
        