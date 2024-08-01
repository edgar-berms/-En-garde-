from carte import *
import random as rd

class Deck:
    def __init__(self):
        self.__deck = []
    
    def remplir(self):
        """
        Rempli le deck de carte. 5 Cartes de chanque valeur.
        """
        for i in range(5):
            j = 0
            while j < 5:
                self.__deck.append(Carte(i+1))
                j = j + 1
    
    def affiche(self):
        """
        Affiche les cartes du deck. 
        """
        print([str(carte) for carte in self.__deck]) 
        print(len(self.__deck))
        
    def swap(self,i,j):
        """
        Echange la position des cartes d'après les indices.
        """
        temp = self.__deck[i]
        self.__deck[i] = self.__deck[j]
        self.__deck[j] = temp
    
    def melange(self):
        """
        Mélange les cartes du deck.
        """
        i = 0
        while i < len(self.__deck):
            self.swap(i,rd.randint(0,len(self.__deck)-1))
            i = i + 1
    
    def retirer_carte(self):
        """
        Supprimer une carte du deck et la renvoie
        """
        return self.__deck.pop()
    
    def est_vide(self):
        """
        Retourne false si le deck est vide, plus de carte à piocher
        """
        return bool(self.__deck)
    
    def vide_deck(self):
        """
        Vide le deck de ses cartes.
        """
        while self.est_vide():
            self.__deck.pop()
            
    def nb_carte_restant(self):
        """
        Retourne le nombre de carte restant dans le deck.
        """
        return len(self.__deck)
            