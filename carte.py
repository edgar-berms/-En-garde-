class Carte:
    def __init__(self,num):
        self.__carte = num
    
    def __str__(self):
        """
        Surdéfinition de la sortie afin de pouvoir afficher des cartes.
        """
        return f"Carte({self.__carte})"
        
    @property
    def get_num(self):
        return self.__carte