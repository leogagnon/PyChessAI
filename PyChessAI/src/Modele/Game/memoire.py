import Modele
from Modele.Game.enums import *


class Memoire:
    """Classe servant de mémoire pour une partie"""

    def __init__(self, game_board):
        # Board de la game
        self.board = game_board

        # [MoveSpecial, numero_move]
        self.memoire_speciale = []

        # [Pièce mangée, numero_move]
        self.memoire_manger = []

        self.numero_move = 0

        # Tous les moves fait depuis le début de la partie
        self.tous_move = []

    def move_made(self, pos_initiale, pos_finale, piece, manger, special, promotion=None):
        """
        Enregistre un move effectué dans la mémoire
        :param pos_initiale: Position initiale
        :param pos_finale: Position finale
        :param piece: Pièce déplacée
        :param manger: Pièce mangée
        :param special: MoveSpecial
        :param promotion: Pièce promue
        """
        self.tous_move.append(Memoire.move_to_string(pos_initiale, pos_finale, piece, promotion))
        if special != MoveSpecial.NULL:
            self.memoire_speciale.append([special, self.numero_move])
        if manger is not None:
            self.memoire_manger.append([manger, self.numero_move])
        self.numero_move += 1

    def undo(self):
        """
        Remet le board à son état précédent
        """
        pos_initiale, pos_finale, piece = self.__undo_transform(self.tous_move.pop())

        if len(self.memoire_manger) != 0 and self.memoire_manger[-1][1] == self.numero_move - 1:
            piece_mangee = self.memoire_manger.pop()[0]
        else :
            piece_mangee = None
        self.board[pos_finale[0]][pos_finale[1]] = piece_mangee
        self.board[pos_initiale[0]][pos_initiale[1]] = piece
        self.board[pos_initiale[0]][pos_initiale[1]].position = pos_initiale[:]

        if len(self.memoire_speciale) != 0 and self.memoire_speciale[-1][1] == self.numero_move - 1:
            special = self.memoire_speciale.pop()[0]
            if special == MoveSpecial.PRISE_EN_PASSANT:  # prise en passant
                self.board[pos_finale[0]][pos_initiale[1]] = Modele.Elements.pion.Pion([pos_finale[0], pos_initiale[1]],
                                                                                     not piece.couleurBlanc)
                self.board[pos_finale[0]][pos_initiale[1]].first = False
            elif special == MoveSpecial.PROMOTION:
                self.board[pos_initiale[0]][pos_initiale[1]] = Modele.Elements.pion.Pion(pos_initiale,piece.couleurBlanc)
                self.board[pos_initiale[0]][pos_initiale[1]].first = False
                self.board[pos_initiale[0]][pos_initiale[1]].second = False
            elif special == MoveSpecial.ROQUE:
                self.board[pos_initiale[0]][pos_initiale[1]].moved = False
                if pos_finale[0] == 6:
                    self.board[7][pos_finale[1]] = Modele.Elements.tour.Tour([7, pos_finale[1]], piece.couleurBlanc)
                    self.board[5][pos_finale[1]] = None
                else:
                    self.board[0][pos_finale[1]] = Modele.Elements.tour.Tour([0, pos_finale[1]], piece.couleurBlanc)
                    self.board[3][pos_finale[1]] = None
            elif special == MoveSpecial.PREMIER_MOUVEMENT_TOUR:
                self.board[pos_initiale[0]][pos_initiale[1]].moved = False
            elif special == MoveSpecial.PREMIER_MOUVEMENT_ROI:
                self.board[pos_initiale[0]][pos_initiale[1]].moved = False
            elif special == MoveSpecial.PREMIER_MOUVEMENT_PION:  # first move of the pawn
                self.board[pos_initiale[0]][pos_initiale[1]].first = True
                self.board[pos_initiale[0]][pos_initiale[1]].second = True
            elif special == MoveSpecial.PRISE_EN_PASSANT_IMPOSSIBLE:
                self.board[pos_initiale[0]][pos_initiale[1]].second = True

        self.numero_move -= 1

    def __undo_transform(self, string_move):
        """
        D'après un string de move, détermine quel a été le move effectué
        :param string_move:
        :return:
        """
        split = string_move.split(":")
        piece_string, move = split[:2]
        lastPosition_string, position_string = move.split("-")

        lastPosition, position = self.string_to_position(lastPosition_string), self.string_to_position(position_string)

        pieceTemp = None
        if piece_string == "R":
            pieceTemp = Modele.Elements.tour.Tour(lastPosition, self.numero_move % 2 == 1)
            pieceTemp.moved = True
        elif piece_string == "K":
            pieceTemp = Modele.Elements.roi.Roi(lastPosition, self.numero_move % 2 == 1)
            pieceTemp.moved = True
        elif piece_string == "Q":
            pieceTemp = Modele.Elements.reine.Reine(lastPosition, self.numero_move % 2 == 1)
        elif piece_string == "N":
            pieceTemp = Modele.Elements.chevalier.Chevalier(lastPosition, self.numero_move % 2 == 1)
        elif piece_string == "B":
            pieceTemp = Modele.Elements.fou.Fou(lastPosition, self.numero_move % 2 == 1)
        elif piece_string == "P":
            pieceTemp = Modele.Elements.pion.Pion(lastPosition, self.numero_move % 2 == 1)
            pieceTemp.first = False
            pieceTemp.second = False
        return [lastPosition, position, pieceTemp]

    @staticmethod
    def string_to_position(algebraic_position):
        """
        Converti une position algébraic en coordonnée cartésienne
        :param algebraic_position: String de la position (ex. a1)
        :return: Coordonnée (ex. [0,0])
        """
        return [ord(algebraic_position[0]) - ord('a'), int(algebraic_position[1]) - 1]

    @staticmethod
    def move_to_string(pos_finale, pos_initiale, piece, promotion):
        """
        Génère un string qui représente un move (ex. P:e7-e8:Q (Pion va de e7 à e8 et effectue une promotion en reine))
        :param pos_finale: Position initiale
        :param pos_initiale: Position finale
        :param piece: Adresse mémoire de la piece initiale (Objet PieceM)
        :param promotion: Adresse mémoire de la piece promue (None si pas de promotion) (Objet PieceM)
        :return:
        """

        if isinstance(piece, Modele.Elements.roi.Roi):
            lettre_piece = 'K'
        elif isinstance(piece, Modele.Elements.reine.Reine):
            lettre_piece = 'Q'
        elif isinstance(piece, Modele.Elements.tour.Tour):
            lettre_piece = 'R'
        elif isinstance(piece, Modele.Elements.chevalier.Chevalier):
            lettre_piece = 'N'
        elif isinstance(piece, Modele.Elements.fou.Fou):
            lettre_piece = 'B'
        else:
            lettre_piece = 'P'

        lettre_promotion = None

        if promotion is not None:

            if isinstance(promotion, Modele.Elements.roi.Roi):
                lettre_promotion = 'K'
            elif isinstance(promotion, Modele.Elements.reine.Reine):
                lettre_promotion = 'Q'
            elif isinstance(promotion, Modele.Elements.tour.Tour):
                lettre_promotion = 'R'
            elif isinstance(promotion, Modele.Elements.chevalier.Chevalier):
                lettre_promotion = 'N'
            elif isinstance(promotion, Modele.Elements.fou.Fou):
                lettre_promotion = 'B'
            else:
                lettre_promotion = 'P'

        return lettre_piece + ":" + chr(ord('a') + pos_initiale[0]) + str(pos_initiale[1] + 1) + "-" + chr(
            ord('a') + pos_finale[0]) + str(pos_finale[1] + 1) + ('' if promotion is None else ":" + lettre_promotion)
