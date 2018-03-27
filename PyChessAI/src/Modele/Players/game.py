from Modele.Players.humain import Humain
from Modele.AI.AlphaBetaPrunning.alphaBeta import AlphaBeta
from Modele.Players.enums import *
import easygui

#Cette classe est en certain terme une façon de storer toutes les informations de deux joueurs
class Game():

    joueur_1 = None
    joueur_2 = None
    tour_blanc = True
    gameMode = None

    def __init__(self, mode_de_jeu, choix_couleur,AI=None):
        Game.gameMode = mode_de_jeu
        Game.initPlayers(choix_couleur)

    #this tell which player is going to be a Machine and which are going to be a humain
    @staticmethod
    def initPlayers(choix_couleur):
        if Game.gameMode is ModeDeJeu.JOUEUR_JOUEUR:
            Game.joueur_1 = Humain(False)
            Game.joueur_2 = Humain(True)
        elif Game.gameMode is ModeDeJeu.JOUEUR_MACHINE:
            Game.joueur_1 = Humain(choix_couleur)
            Game.joueur_2 = Game.chooseTypeAI(not choix_couleur)
        elif Game.gameMode is ModeDeJeu.MACHINE_MACHINE:
            Game.joueur_1 = Game.chooseTypeAI(True)
            Game.joueur_2 = Game.chooseTypeAI(False)

    #Cette méthode va faire en sorte que nous pouvons savoir quel type de AI jouera
    @staticmethod
    def chooseTypeAI(couleur):
        type = AlphaBeta(couleur)
        return type

    #ask the user what color he wants to play against the AI
    @staticmethod
    def decidingCouleur():
        return easygui.boolbox('Choix de couleur','',['Blanc','Noir'])

    #Va sortir le player à qui c'est le tour
    @staticmethod
    def get_tour():
        if Game.joueur_1.COULEUR_BLANC is Game.tour_blanc:
            return Game.joueur_1
        return Game.joueur_2

