from Modele.Game.humain import Humain
from Modele.Game.machine import Machine
from Modele.AI.AlphaBetaPrunning.alphaBeta import AlphaBeta
from Modele.Game.enums import *
from Modele.Game.machine import TypeAI
from Modele.AI.Stockfish9.stockfish import Stockfish
from Modele.AI.LeelaChessZero.lczero import LCZero
from Modele.Elements.memoire import Memoire
class Game:
    """Classe contenant les informations nécéssaires au déroulement d'une partie"""



    def __init__(self, mode_de_jeu, choix_couleur, AI_1=None, depth_1=None, AI_2=None, depth_2=None):

        self.memoire = Memoire()
        self.board = [[None for _ in range(8)] for _ in range(8)]

        self.joueur_1 = None
        self.joueur_2 = None
        self.tour_blanc = True
        self.mode_de_jeu = mode_de_jeu
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

        if self.mode_de_jeu is ModeDeJeu.JOUEUR_JOUEUR:
            self.joueur_1 = Humain(False)
            self.joueur_2 = Humain(True)
        elif self.mode_de_jeu is ModeDeJeu.JOUEUR_MACHINE:
            self.joueur_1 = Humain(choix_couleur)
            self.joueur_2 = self.init_ai(AI_1, not choix_couleur, depth_1)
        elif self.mode_de_jeu is ModeDeJeu.MACHINE_MACHINE:
            self.joueur_1 = self.init_ai(AI_1, choix_couleur, depth_1)
            self.joueur_2 = self.init_ai(AI_2, not choix_couleur, depth_2)

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
            return Stockfish(couleur, depth)
        elif type_ai is TypeAI.ALPHA_ZERO:
            return #AlphaZero(couleur)
        elif type_ai is TypeAI.LCZERO:
            return LCZero(couleur)

    def get_active_player(self):
        """
        Indique à qui est le tour
        :return: Revoie un objet Joueur()
        """
        if self.joueur_1.COULEUR_BLANC is self.tour_blanc:
            return self.joueur_1
        return self.joueur_2

    def move(self, position, lastPosition, piece, manger, special):
        """

        :param lastPosition:
        :param piece:
        :param manger:
        :param special:
        :return:
        """

        self.memoire.move_made(position, lastPosition, piece, manger, special)
        self.tour_blanc = not self.tour_blanc

    def undo(self):

        self.memoire.undo(self.board)
        self.tour_blanc = not self.tour_blanc

    def next(self):

        player = self.get_active_player()
        best_move = None

        if (isinstance(player, Machine)):
            lastPosition, position = player.play(self.board, self.memoire.tous_move)

            pieceTemp = self.board[position[0]][position[1]]
            special = self.board[lastPosition[0]][lastPosition[1]].mouvementMemory(position,lastPosition,self.board)
            self.move(position, lastPosition,self.board[position[0]][position[1]], pieceTemp, special)
        else:
            print('Un humain a besoin de jouer avant la machine')
