from Modele.Game.humain import Humain
from Modele.Game.machine import Machine
from Modele.AI.AlphaBetaPrunning.alphaBeta import AlphaBeta
from Modele.Game.enums import *
from Modele.Game.machine import TypeAI
from Modele.AI.Stockfish9.stockfish import Stockfish
from Modele.AI.LeelaChessZero.lczero import LCZero
from Modele.Elements.memoire import Memoire
from Modele.Elements.fou import Fou
from Modele.Elements.reine import Reine
from Modele.Elements.chevalier import Chevalier
from Modele.Elements.tour import Tour
from Modele.Elements.pion import Pion
from Modele.Elements.roi import Roi


class Game:
    """Classe contenant les informations nécéssaires au déroulement d'une partie"""

    def __init__(self, mode_de_jeu, choix_couleur=None, AI_1=None, depth_1=None, AI_2=None, depth_2=None):

        self.memoire = Memoire()
        self.board = [[None for _ in range(8)] for _ in range(8)]

        self.joueur_1 = None
        self.joueur_2 = None
        self.tour_blanc = True
        self.mode_de_jeu = mode_de_jeu
        self.initPlayers(choix_couleur, AI_1, depth_1, AI_2, depth_2)

    def initPlayers(self, choix_couleur, AI_1, depth_1, AI_2, depth_2):
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
            self.joueur_1 = self.init_ai(AI_1, True, depth_1)
            self.joueur_2 = self.init_ai(AI_2, False, depth_2)

    def init_ai(self, type_ai, couleur, depth):

        """
        Initialise un AI et le retourne
        :param type_ai: Type
        :param couleur: Couleur
        :param depth: Profondeur d'évaluation
        :return: Un objet Machine() (Le AI)
        """
        if type_ai is TypeAI.ALPHA_BETA:
            return AlphaBeta(couleur, depth, self.memoire)
        elif type_ai is TypeAI.NEURAL_NETWORK:
            return  # NeuralNetwork(couleur)
        elif type_ai is TypeAI.STOCKFISH:
            return Stockfish(couleur, depth, self.memoire)
        elif type_ai is TypeAI.LCZERO:
            return LCZero(couleur, self.memoire)

    def get_active_player(self):
        """
        Indique à qui est le tour
        :return: Revoie un objet Joueur()
        """
        if self.joueur_1.COULEUR_BLANC is self.tour_blanc:
            return self.joueur_1
        return self.joueur_2

    def move(self, pos_finale, pos_initiale):
        """
        Effectue un move et change le tour
        :param pos_finale:
        :param pos_initiale:
        :return:
        """

        piece = self.board[pos_initiale[0]][pos_initiale[1]]
        manger = self.board[pos_finale[0]][pos_finale[1]]
        special = self._make_move(pos_finale, pos_initiale)
        promotion = None

        if special is MoveSpecial.PROMOTION:
            promotion = self.board[pos_finale[0]][pos_finale[1]]

        self.memoire.move_made(pos_finale, pos_initiale, piece, manger, special, promotion=promotion)
        self.tour_blanc = not self.tour_blanc

    def undo(self):
        """
        Reviens un move en arrière et change le tour
        """
        self.memoire.undo(self.board)
        self.tour_blanc = not self.tour_blanc

    def next(self):
        """
        Passe au prochain tour en faisant jouer une machine
        """
        player = self.get_active_player()

        if isinstance(player, Machine):
            pos_initiale, pos_finale = player.play(self.board)
            self.move(pos_finale, pos_initiale)
        else:
            print('Un humain a besoin de jouer avant la machine !')

    def promotion(self, position):

        """
        Effectue la promotion
        :param position: Position de la pièce à promouvoir
        """
        player = self.get_active_player()
        choix = player.get_promotion()

        if choix == TypePiece.REINE:
            self.board[position[0]][position[1]] = Reine(position, player.COULEUR_BLANC)
        elif choix == TypePiece.TOUR:
            self.board[position[0]][position[1]] = Tour(position, player.COULEUR_BLANC)
        elif choix == TypePiece.CAVALIER:
            self.board[position[0]][position[1]] = Chevalier(position, player.COULEUR_BLANC)
        elif choix == TypePiece.FOU:
            self.board[position[0]][position[1]] = Fou(position, player.COULEUR_BLANC)

    def _make_move(self, pos_finale, pos_initiale):

        """
        Effectue un move dans le board en prenant en compte les mouvements spéciaux
        :param pos_finale: Position finale de la pièce
        :param pos_initiale: Position initiale de la pièce
        :return: Type de mouvement spécial
        """
        # Valeur spéciale par défaut
        special = MoveSpecial.NULL

        # Vérifie si une prise en passant est en cours et élimine le pion si c'est le cas
        if isinstance(self.board[pos_initiale[0]][pos_initiale[1]], Pion):
            if abs(pos_finale[0] - pos_initiale[0]) == 1 and self.board[pos_finale[0]][pos_finale[1]] == None:
                self.board[pos_finale[0]][pos_initiale[1]] = None
                special = MoveSpecial.PRISE_EN_PASSANT

        # Effectue le mouvement dans self.board
        self.board[pos_finale[0]][pos_finale[1]] = self.board[pos_initiale[0]][pos_initiale[1]]
        self.board[pos_finale[0]][pos_finale[1]].position = pos_finale
        self.board[pos_initiale[0]][pos_initiale[1]] = None

        if isinstance(self.board[pos_finale[0]][pos_finale[1]], Pion):
            if self.board[pos_finale[0]][pos_finale[1]].first:
                self.board[pos_finale[0]][pos_finale[1]].first = False
                special = MoveSpecial.PREMIER_MOUVEMENT_PION
            elif self.board[pos_finale[0]][pos_finale[1]].second:
                special = MoveSpecial.PRISE_EN_PASSANT_IMPOSSIBLE
                # Effectue la prise en passant
                if isinstance(self.board[pos_finale[0]][pos_finale[1]], Pion):
                    if self.board[pos_finale[0]][pos_finale[1]].first:
                        for temp in self.board:
                            for temp2 in temp:
                                if isinstance(temp2, Pion) and temp2.second:
                                    temp2.second = False
                        self.board[pos_finale[0]][pos_finale[1]].first = False
                        if abs(pos_initiale[1] - pos_finale[1]) == 2:
                            self.board[pos_finale[0]][pos_finale[1]].second = True
                    elif self.board[pos_finale[0]][pos_finale[1]].second:
                        self.board[pos_finale[0]][pos_finale[1]].second = False
                else:
                    for temp in self.board:
                        for temp2 in temp:
                            if isinstance(temp2, Pion) and temp2.second:
                                temp2.second = False

        if isinstance(self.board[pos_finale[0]][pos_finale[1]], Pion):
            if pos_finale[1] == 7 or pos_finale[1] == 0:
                self.promotion(pos_finale)
                special = MoveSpecial.PROMOTION
        elif isinstance(self.board[pos_finale[0]][pos_finale[1]], Tour):
            if not (self.board[pos_finale[0]][pos_finale[1]].moved):
                self.board[pos_finale[0]][pos_finale[1]].moved = True
                special = MoveSpecial.PREMIER_MOUVEMENT_TOUR
        elif isinstance(self.board[pos_finale[0]][pos_finale[1]], Roi):
            if not self.board[pos_finale[0]][pos_finale[1]].moved:
                special = MoveSpecial.PREMIER_MOUVEMENT_ROI
                if pos_initiale[0] - pos_finale[0] == -2:
                    self._make_move([pos_finale[0] - 1, pos_finale[1]], [7, pos_finale[1]])
                    special = MoveSpecial.ROQUE
                elif pos_initiale[0] - pos_finale[0] == 2:
                    self._make_move([pos_finale[0] + 1, pos_finale[1]], [0, pos_finale[1]])
                    special = MoveSpecial.ROQUE
                self.board[pos_finale[0]][pos_finale[1]].moved = True

        return special
