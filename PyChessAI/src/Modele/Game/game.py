from Modele.Game.humain import Humain
from Modele.Game.machine import Machine
from Modele.AI.AlphaBetaPrunning.alphaBeta import AlphaBeta
from Modele.Game.enums import *
from Modele.Game.machine import TypeAI
from Modele.AI.Stockfish9.stockfish9 import Stockfish9


class Game():
    """Classe contenant les informations nécéssaires au déroulement d'une partie"""

    joueur_1 = None
    joueur_2 = None
    tour_blanc = True
    mode_de_jeu = None

    def __init__(self, mode_de_jeu, choix_couleur, AI_1=None, depth_1=None, AI_2=None, depth_2=None):

        Game.mode_de_jeu = mode_de_jeu
        self.initPlayers(choix_couleur, AI_1, depth_1, AI_2, depth_2)

    def initPlayers(self,choix_couleur, AI_1, depth_1, AI_2, depth_2):
        '''
        Initialise les deux joueurs
        :param choix_couleur: Couleur choisise par le joueur (Seulement utile pour JOUEUR_MACHINE)
        :param AI_1: Type du premier AI
        :param depth_1: Profondeur d'évaluation du premier AI
        :param AI_2: Type du deuxième AI
        :param depth_2: Profondeur d'évaluation du deuxième AI
        '''

        if Game.mode_de_jeu is ModeDeJeu.JOUEUR_JOUEUR:
            Game.joueur_1 = Humain(False)
            Game.joueur_2 = Humain(True)
        elif Game.mode_de_jeu is ModeDeJeu.JOUEUR_MACHINE:
            Game.joueur_1 = Humain(choix_couleur)
            Game.joueur_2 = self.init_ai(AI_1, not choix_couleur, depth_1)
        elif Game.mode_de_jeu is ModeDeJeu.MACHINE_MACHINE:
            Game.joueur_1 = self.init_ai(AI_1, choix_couleur, depth_1)
            Game.joueur_2 = self.init_ai(AI_2, not choix_couleur, depth_2)

    def init_ai(self, type_ai, couleur, depth):

        """
        Initialise un AI et le retourne
        :param type_ai: Type
        :param couleur: Couleur
        :param depth: Profondeur d'évaluation
        :return: Un objet Machine() (Le AI)
        """
        if type_ai is TypeAI.MINIMAX:
            return #MiniMax(couleur,depth)
        elif type_ai is TypeAI.ALPHA_BETA:
            return AlphaBeta(couleur,depth)
        elif type_ai is TypeAI.NEURAL_NETWORK:
            return #NeuralNetwork(couleur)
        elif type_ai is TypeAI.STOCKFISH:
            return Stockfish9(couleur,depth)
        elif type_ai is TypeAI.ALPHA_ZERO:
            return #AlphaZero(couleur)

    @staticmethod
    def get_active_player():
        """
        Indique à qui est le tour
        :return: Revoie un objet Joueur()
        """
        if Game.joueur_1.COULEUR_BLANC is Game.tour_blanc:
            return Game.joueur_1
        return Game.joueur_2
