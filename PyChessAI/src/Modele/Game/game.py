from Modele.Elements.chevalier import Chevalier
from Modele.Elements.fou import Fou
from Modele.Elements.pion import Pion
from Modele.Elements.reine import Reine
from Modele.Elements.roi import Roi
from Modele.Elements.tour import Tour
from Modele.Engines.AlphaBetaPrunning.alphaBeta import AlphaBeta
from Modele.Engines.LeelaChessZero.lczero import LCZero
from Modele.Engines.Stockfish9.stockfish import Stockfish
from Modele.Game.enums import *
from Modele.Game.humain import Humain
from Modele.Game.machine import Machine
from Modele.Game.machine import TypeEngine
from Modele.Game.memoire import Memoire
from Modele.Engines.Komodo.komodo import Komodo
from Modele.Engines.Gull.gull import Gull


class Game:
    """Classe contenant les informations nécéssaires au déroulement d'une partie"""

    def __init__(self, mode_de_jeu, choix_couleur=None, AI_1=None, depth_1=None, AI_2=None, depth_2=None):

        # Board contenant les pièces du jeu
        self.board = [[None for _ in range(8)] for _ in range(8)]

        # Memoire des moves
        self.memoire = Memoire(self.board)

        # Joueurs
        self.joueur_1 = None
        self.joueur_2 = None

        # Indique à qui est le tour : True -> Blanc, False -> Noirs
        self.tour_blanc = True

        # Indique le mode de jeu
        self.mode_de_jeu = mode_de_jeu

        self.__init_joueurs(choix_couleur, AI_1, depth_1, AI_2, depth_2)

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
        special = self.__make_move(pos_finale, pos_initiale)
        promotion = None

        if special is MoveSpecial.PROMOTION:
            promotion = self.board[pos_finale[0]][pos_finale[1]]

        self.memoire.move_made(pos_finale, pos_initiale, piece, manger, special, promotion=promotion)
        self.tour_blanc = not self.tour_blanc

    def undo(self):
        """
        Reviens un move en arrière et change le tour
        """

        self.memoire.undo()
        self.tour_blanc = not self.tour_blanc

    def next(self):
        """
        Passe au prochain tour en faisant jouer une machine
        """

        player = self.get_active_player()

        if isinstance(player, Machine):
            pos_initiale, pos_finale = player.play()
            self.move(pos_finale, pos_initiale)
        else:
            print('Un humain a besoin de jouer avant la machine !')

    def __promotion(self, position):
        """
        Effectue la __promotion
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

    def __make_move(self, pos_finale, pos_initiale):
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
                self.__promotion(pos_finale)
                special = MoveSpecial.PROMOTION
        elif isinstance(self.board[pos_finale[0]][pos_finale[1]], Tour):
            if not (self.board[pos_finale[0]][pos_finale[1]].moved):
                self.board[pos_finale[0]][pos_finale[1]].moved = True
                special = MoveSpecial.PREMIER_MOUVEMENT_TOUR
        elif isinstance(self.board[pos_finale[0]][pos_finale[1]], Roi):
            if not self.board[pos_finale[0]][pos_finale[1]].moved:
                special = MoveSpecial.PREMIER_MOUVEMENT_ROI
                if pos_initiale[0] - pos_finale[0] == -2:
                    self.__make_move([pos_finale[0] - 1, pos_finale[1]], [7, pos_finale[1]])
                    special = MoveSpecial.ROQUE
                elif pos_initiale[0] - pos_finale[0] == 2:
                    self.__make_move([pos_finale[0] + 1, pos_finale[1]], [0, pos_finale[1]])
                    special = MoveSpecial.ROQUE
                self.board[pos_finale[0]][pos_finale[1]].moved = True

        return special

    def __init_joueurs(self, choix_couleur, engine_1, depth_1, engine_2, depth_2):
        '''
        Initialise les deux joueurs
        :param choix_couleur: Couleur choisise par le joueur (Seulement utile pour JOUEUR_MACHINE)
        :param engine_1: Type du premier engine
        :param depth_1: Profondeur d'évaluation du premier engine
        :param engine_2: Type du deuxième Engines
        :param depth_2: Profondeur d'évaluation du deuxième Engines
        '''

        if self.mode_de_jeu is ModeDeJeu.JOUEUR_JOUEUR:
            self.joueur_1 = Humain(False)
            self.joueur_2 = Humain(True)
        elif self.mode_de_jeu is ModeDeJeu.JOUEUR_MACHINE:
            self.joueur_1 = Humain(choix_couleur)
            self.joueur_2 = self.__init_engine(engine_1, not choix_couleur, depth_1)
        elif self.mode_de_jeu is ModeDeJeu.MACHINE_MACHINE:
            self.joueur_1 = self.__init_engine(engine_1, True, depth_1)
            self.joueur_2 = self.__init_engine(engine_2, False, depth_2)

    def __init_engine(self, type_engine, couleur, depth):
        """
        Initialise un engine et le retourne
        :param type_engine: Type
        :param couleur: Couleur
        :param depth: Profondeur d'évaluation
        :return: Un objet Machine()
        """

        if type_engine is TypeEngine.ALPHA_BETA:
            return AlphaBeta(couleur, depth, self)
        elif type_engine is TypeEngine.NEURAL_NETWORK:
            return  # NeuralNetwork(couleur)
        elif type_engine is TypeEngine.STOCKFISH:
            return Stockfish(couleur, depth, self)
        elif type_engine is TypeEngine.LCZERO:
            return LCZero(couleur, self)
        elif type_engine is TypeEngine.KOMODO:
            return Komodo(couleur, depth, self)
        elif type_engine is TypeEngine.GULL:
            return Gull(couleur, depth, self)
