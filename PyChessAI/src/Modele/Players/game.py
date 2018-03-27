from Modele.Players.humain import Humain
from Modele.Players.machine import Machine
from Modele.AI.AlphaBetaPrunning.alphaBeta import AlphaBeta
from Modele.Players.enums import *
from Modele.Players.machine import TypeAI
import easygui


# Cette classe est en certain terme une façon de storer toutes les informations de deux joueurs
class Game():
    joueur_1 = None
    joueur_2 = None
    tour_blanc = True
    gameMode = None

    def __init__(self, mode_de_jeu, choix_couleur, AI_1=None, AI_2=None):
        Game.gameMode = mode_de_jeu
        Game.initPlayers(choix_couleur, AI_1, AI_2)

    # this tell which player is going to be a Machine and which are going to be a humain
    @staticmethod
    def initPlayers(choix_couleur, AI_1, AI_2):


        if Game.gameMode is ModeDeJeu.JOUEUR_JOUEUR:
            Game.joueur_1 = Humain(False)
            Game.joueur_2 = Humain(True)
        elif Game.gameMode is ModeDeJeu.JOUEUR_MACHINE:
            Game.joueur_1 = Humain(choix_couleur)
            Game.joueur_2 = Game.init_ai(AI_1,not choix_couleur)
        elif Game.gameMode is ModeDeJeu.MACHINE_MACHINE:
            Game.joueur_1 = Game.init_ai(AI_1,choix_couleur)
            Game.joueur_2 = Game.init_ai(AI_2,not choix_couleur)

    # Cette méthode va faire en sorte que nous pouvons savoir quel type de AI jouera
    @staticmethod
    def init_ai(type_ai, couleur):

        if type_ai is TypeAI.MINIMAX:
            return
        elif type_ai is TypeAI.ALPHA_BETA:
            return AlphaBeta(couleur)
        elif type_ai is TypeAI.NEURAL_NETWORK:
            return
        elif type_ai is TypeAI.STOCKFISH:
            return
        elif type_ai is TypeAI.ALPHA_ZERO:
            return



    # Va sortir le player à qui c'est le tour
    @staticmethod
    def get_tour():
        if Game.joueur_1.COULEUR_BLANC is Game.tour_blanc:
            return Game.joueur_1
        return Game.joueur_2
