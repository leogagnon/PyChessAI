from Modele.Players.humain import Humain
from Modele.Players.machine import Machine
from Modele.AI.AlphaBetaPrunning.alphaBeta import AlphaBeta
from Modele.Players.enums import *
from Modele.Players.machine import TypeAI
from Modele.AI.Stockfish9.stockfish9 import Stockfish9
import easygui


# Cette classe est en certain terme une façon de storer toutes les informations de deux joueurs
class Game():
    joueur_1 = None
    joueur_2 = None
    tour_blanc = True
    gameMode = None

    def __init__(self, mode_de_jeu, choix_couleur, AI_1=None, depth_1=None, AI_2=None, depth_2=None):
        Game.gameMode = mode_de_jeu
        Game.initPlayers(choix_couleur, AI_1, depth_1, AI_2, depth_2)


    @staticmethod
    def initPlayers(choix_couleur, AI_1, depth_1, AI_2, depth_2):
        '''
        Initialise les deux joueurs
        :param choix_couleur: Couleur choisise par le joueur (Seulement utile pour JOUEUR_MACHINE)
        :param AI_1: Type du premier AI
        :param AI_2: Type du deuxième AI
        '''

        if Game.gameMode is ModeDeJeu.JOUEUR_JOUEUR:
            Game.joueur_1 = Humain(False)
            Game.joueur_2 = Humain(True)
        elif Game.gameMode is ModeDeJeu.JOUEUR_MACHINE:
            Game.joueur_1 = Humain(choix_couleur)
            Game.joueur_2 = Game.init_ai(AI_1, not choix_couleur, depth_1)
        elif Game.gameMode is ModeDeJeu.MACHINE_MACHINE:
            Game.joueur_1 = Game.init_ai(AI_1, choix_couleur, depth_1)
            Game.joueur_2 = Game.init_ai(AI_2, not choix_couleur, depth_2)

    @staticmethod
    def init_ai(type_ai, couleur, depth):

        """
        Initialise un AI et le retourne
        :param type_ai: Type du AI
        :param couleur: Couleur du AI
        :return: Un objet machine (Le AI)
        """
        if type_ai is TypeAI.MINIMAX:
            return
        elif type_ai is TypeAI.ALPHA_BETA:
            return AlphaBeta(couleur,depth)
        elif type_ai is TypeAI.NEURAL_NETWORK:
            return
        elif type_ai is TypeAI.STOCKFISH:
            return Stockfish9(couleur,depth)
        elif type_ai is TypeAI.ALPHA_ZERO:
            return

    @staticmethod
    def get_tour():
        """
        Indique à qui est le tour
        :return: Revoie un objet Joueur()
        """
        if Game.joueur_1.COULEUR_BLANC is Game.tour_blanc:
            return Game.joueur_1
        return Game.joueur_2
