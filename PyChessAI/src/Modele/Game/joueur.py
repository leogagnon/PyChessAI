from abc import ABC, abstractmethod  # pour faire des classes et des méthodes abstraites
import Modele


#C'est la classe qui va contenir les informations générales que le AI ou le joueur Humain doivent posséder
class Joueur(ABC):
    # constructeur
    def __init__(self, couleur_blanc):
        self.COULEUR_BLANC = couleur_blanc

    #Chaqu'un doit avoir une façon de décider de son choix de promotion
    @abstractmethod
    def choix_promotion(self, board, position):
        """
        Permet de décider le choix de promotion
        :param board: État du board
        :param position: Position de la piece
        """
        pass
