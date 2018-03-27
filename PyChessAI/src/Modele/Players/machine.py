from Modele.Players.joueur import Joueur
from Modele.Elements.pion import Pion
from abc import ABC, abstractclassmethod
from enum import Enum
import Modele


class TypeAI(Enum):
    MINIMAX = 0
    ALPHA_BETA = 1
    NEURAL_NETWORK = 2
    STOCKFISH = 3
    ALPHA_ZERO = 4


# Voici la classe abstraite pour tous nos AI (vu que ceux-ci doivent partager des caractéristiques communes)
class Machine(Joueur, ABC):
    # constructeur
    def __init__(self, couleur):
        super().__init__(couleur)
        self.position = None
        self.lastPosition = None

    # Cela est une méthode abstraite qui va faire en sorte de rouler l'algorithme du AI sélectionner par l'usager
    @abstractclassmethod
    def play(self, board):
        pass

    # Cela dit que le choix que le AI fait pour la promotion est une dame (dans les games sérieuses c'est 99% du temps un dame)
    def choix_promotion(self, board, position):
        return Pion.getChoices()[0]
