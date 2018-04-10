from Modele.Game.joueur import Joueur
from Modele.Elements.pion import Pion
from abc import ABC, abstractclassmethod
from enum import Enum
import Modele


class TypeAI(Enum):
    ALPHA_BETA = 'MiniMax avec étalonage alpha-bêta'
    NEURAL_NETWORK = 'Neural Network'
    STOCKFISH = 'Stockfish9'
    LCZERO = 'Leela Chess Zero'


# Voici la classe abstraite pour tous nos AI (vu que ceux-ci doivent partager des caractéristiques communes)
class Machine(Joueur, ABC):
    # constructeur
    def __init__(self, couleur, memoire):
        self.promotion = None
        self.position = None
        self.lastPosition = None
        self.memoire = memoire
        super().__init__(couleur)

    # Cela est une méthode abstraite qui va faire en sorte de rouler l'algorithme du AI sélectionner par l'usager
    @abstractclassmethod
    def play(self, board, memoire):
        pass

    def get_promotion(self):
        return self.promotion
