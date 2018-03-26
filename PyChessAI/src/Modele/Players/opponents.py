from Modele.Players.humain import Humain
from Modele.AI.AlphaBetaPrunning.alphaBeta import AlphaBeta

#Cette classe est en certain terme une façon de storer toutes les informations de deux joueurs
class Opponents():
    player1 = None
    player2 = None
    tour_blanc = True #c'est le tour de quelle couleur
    gameMode = -1 # gameMode == 0 -> player vs player ;  1 -> player vs AI ; 2 -> AI vs AI
    screen = None # pour afficher sur le screen (si on veut demander une question à l'utilisateur)

    def __init__(self, gameNumber, screen):
        Opponents.gameMode = gameNumber
        Opponents.initPlayers()
        Opponents.screen = screen

    #this tell which player is going to be a Cpu and which are going to be a humain
    @staticmethod
    def initPlayers():
        if Opponents.gameMode == 0:
            Opponents.player1 = Humain(False)
            Opponents.player2 = Humain(True)
        elif Opponents.gameMode == 1:
            couleur_humain = Opponents.decidingCouleur()
            Opponents.player1 = Humain(couleur_humain)
            Opponents.player2 = Opponents.chooseTypeAI(not couleur_humain)
        else:
            Opponents.player1 = Opponents.chooseTypeAI(True)
            Opponents.player2 = Opponents.chooseTypeAI(False)

    #Cette méthode va faire en sorte que nous pouvons savoir quel type de AI jouera
    @staticmethod
    def chooseTypeAI(couleur):
        type = AlphaBeta(couleur)
        return type

    #ask the user what color he wants to play against the AI
    @staticmethod
    def decidingCouleur():
        return True

    #Va sortir True si c'est le tour d'un Humain et va sortir False si c'est le tour d'un AI
    @staticmethod
    def playerTourHumain():
        if Opponents.player1.sonTour():
            if isinstance(Opponents.player1, Humain):
                return True
            return False
        if isinstance(Opponents.player2, Humain):
            return True
        return False

    #Va sortir le player à qui c'est le tour
    @staticmethod
    def getPlayerTour():
        if Opponents.player1.sonTour():
            return Opponents.player1
        return Opponents.player2

