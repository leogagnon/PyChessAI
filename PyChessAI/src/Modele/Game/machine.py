from Modele.Game.joueur import Joueur
from Modele.Elements.pion import Pion
from abc import ABC, abstractclassmethod
from enum import Enum
import Modele


class TypeAI(Enum):
    MINIMAX = 'Minimax'
    ALPHA_BETA = 'MiniMax avec étalonage alpha-bêta'
    NEURAL_NETWORK = 'Neural Network'
    STOCKFISH = 'Stockfish9'
    ALPHA_ZERO = 'Alpha Zero (Google)'


# Voici la classe abstraite pour tous nos AI (vu que ceux-ci doivent partager des caractéristiques communes)
class Machine(Joueur, ABC):
    # constructeur
    def __init__(self, couleur, depth):
        self.position = None
        self.lastPosition = None
        self.depth = depth
        super().__init__(couleur)

    # Cela est une méthode abstraite qui va faire en sorte de rouler l'algorithme du AI sélectionner par l'usager
    @abstractclassmethod
    def play(self, board):
        pass

    # Cela dit que le choix que le AI fait pour la promotion est une dame (dans les games sérieuses c'est 99% du temps un dame)
    def choix_promotion(self, board, position):
        return Pion.getChoices()[0]
