from Modele.Game.joueur import Joueur
from abc import ABC, abstractclassmethod
from enum import Enum
import Modele


class TypeEngine(Enum):
    ALPHA_BETA = 'MiniMax avec étalonage alpha-bêta'
    NEURAL_NETWORK = 'Neural Network'
    STOCKFISH = 'Stockfish9'
    LCZERO = 'Leela Chess Zero'
    MINIMAX = 'MiniMax classique'
    KOMODO = 'Komodo'
    GULL = 'Gull'

# Voici la classe abstraite pour tous nos Engines (vu que ceux-ci doivent partager des caractéristiques communes)
class Machine(Joueur, ABC):
    def __init__(self, couleur, game):

        #Contient le choix de promotion qui vient d'être fait (None si aucun)
        self.promotion = None

        #Game dont la machine fait partie
        self.game = game

        super().__init__(couleur)

    @abstractclassmethod
    def play(self):
        """
        Méthode appelée pour faire jouer un coup au engine
        :return: Le meilleur move
        """
        pass

    def get_promotion(self):
        return self.promotion
