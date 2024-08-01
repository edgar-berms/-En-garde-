class Joueur:
    def __init__(self,nom,couleur):
        self.__nom = nom
        self.__main = []
        self.__couleur = couleur
        self.__commence = False
        self.__score = 0
        self.__position = 0
        self.__temp = 0
    
    #Getter et setter pour les principaux attributs de la classe Joueur
    @property
    def get_nom(self):
        return self.__nom
    @property
    def get_couleur(self):
        return self.__couleur
    @property
    def get_commence(self):
        return self.__commence
    @property
    def get_score(self):
        return self.__score
    @property
    def get_position(self):
        return self.__position
    @property
    def get_temp(self):
        return self.__temp
    @property
    def get_main(self):
        return self.__main
    @get_score.setter
    def set_score(self,n):
        self.__score = n
    @get_nom.setter
    def set_nom(self,n):
        self.__nom = n
    @get_couleur.setter
    def set_couleur(self,c):
        self.__couleur = c
    @get_commence.setter
    def set_commence(self,b):
        self.__commence = b
    @get_position.setter
    def set_position(self,n):
        if(n > 23):
            print("msg erreur")
        else:
            self.__position = n
    @get_temp.setter
    def set_temp(self,n):
        self.__temp = n
        
        
    def affiche(self):
        """
        Affiche les proprietés d'un joueur.
        """
        print(self.__nom, "est representé par la couleur", self.__couleur)
    
    def affiche_main(self):
        """
        Affiche la main actuel d'un joueur.
        """
        print([str(carte) for carte in self.__main])
        
    def score_plus_un(self):
        """
        Rajoute 1 point au niveau des scores au gagnant.
        """
        self.__score = self.__score + 1
        
    def ajout_main(self,n):
        """
        Ajoute une carte dans la main du joueur.
        """
        self.__main.append(n)
        
    def sup_main(self,n):
        """
        Supprime une carte de la main avec l'indice de la carte.
        """
        self.__main.pop(n)
    
    def get_carte_main(self,index):
        """
        Retourne une carte de la main avec son index en paramètre.
        """
        return self.__main[index]
    
    def vide_main(self):
        """
        Vide la main du joueur.
        """
        while self.__main:
            self.sup_main(0)