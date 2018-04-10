import Modele
from Modele.Game.enums import *


#cette classe est utile pour undo (ce qui sera utile dans chaque mode_de_jeu)
#les deux méthode qui vont être utile en dehors de la classe sont move_made et undo


class Memoire:

    def __init__(self, game_board):
        #Board de la game
        self.board = game_board

        # [MoveSpecial, numero_move]
        self.memoire_speciale = []

        # [Pièce mangée, numero_move]
        self.memoire_manger = []

        self.numero_move = 0

        # Tous les moves fait depuis le début de la partie
        self.tous_move = []

    # !!! c'est important d'appeler cette méthode pour pouvoir avoir la capacité de undo
    def move_made(self,position, lastPosition, piece, manger, special, promotion=None):
        self.tous_move.append(Memoire.transform(position, lastPosition, piece, promotion))
        if special != MoveSpecial.NULL:
            self.memoire_speciale.append([special, self.numero_move])
        if manger is not None:
            self.memoire_manger.append([manger, self.numero_move])
        self.numero_move += 1

    def undo(self):
        """
        Remet le board à son état précédent
        """
        lastPosition, position, pieceBouger = self.undo_transform(self.tous_move.pop()) #lastPosition, position, piece qui a été bouger

        tempPiece = None
        if len(self.memoire_manger) != 0 and self.memoire_manger[-1][1] == self.numero_move - 1:
            tempPiece = self.memoire_manger.pop()[0]
        self.board[position[0]][position[1]] = tempPiece
        self.board[lastPosition[0]][lastPosition[1]] = pieceBouger
        self.board[lastPosition[0]][lastPosition[1]].position = lastPosition[:]

        if len(self.memoire_speciale) != 0 and self.memoire_speciale[-1][1] == self.numero_move - 1:
            special = self.memoire_speciale.pop()[0]
            if special == MoveSpecial.PRISE_EN_PASSANT:#prise en passant
                self.board[position[0]][lastPosition[1]] = Modele.Elements.pion.Pion([position[0], lastPosition[1]], not pieceBouger.couleurBlanc)
                self.board[position[0]][lastPosition[1]].first = False
            elif special == MoveSpecial.PROMOTION: # _promotion
                self.board[lastPosition[0]][lastPosition[1]] = Modele.Elements.pion.Pion(lastPosition, pieceBouger.couleurBlanc)
                self.board[lastPosition[0]][lastPosition[1]].first = False
                self.board[lastPosition[0]][lastPosition[1]].second = False
            elif special == MoveSpecial.ROQUE:#roque
                self.board[lastPosition[0]][lastPosition[1]].moved = False
                if position[0] == 6:
                    self.board[7][position[1]] = Modele.Elements.tour.Tour([7,position[1]], pieceBouger.couleurBlanc)
                    self.board[5][position[1]] = None
                else:
                    self.board[0][position[1]] = Modele.Elements.tour.Tour([0,position[1]], pieceBouger.couleurBlanc)
                    self.board[3][position[1]] = None
            elif special == MoveSpecial.PREMIER_MOUVEMENT_TOUR: #the rook has been moved for the first time
                self.board[lastPosition[0]][lastPosition[1]].moved = False
            elif special == MoveSpecial.PREMIER_MOUVEMENT_ROI: #the king has been moved for the first time and did not do the roque
                self.board[lastPosition[0]][lastPosition[1]].moved = False
            elif special == MoveSpecial.PREMIER_MOUVEMENT_PION: #first move of the pawn
                self.board[lastPosition[0]][lastPosition[1]].first = True
                self.board[lastPosition[0]][lastPosition[1]].second = True
            elif special == MoveSpecial.PRISE_EN_PASSANT_IMPOSSIBLE: #the pawn could do his second move
                self.board[lastPosition[0]][lastPosition[1]].second = True

        self.numero_move -= 1

    #prendre le string qui a été noté et output le move qui a été fait et avec quelle pièce
    def undo_transform(self, string_move):
        #Ignore les promotions : P:e7-e8(:Q)
        split = string_move.split(":")
        piece_string, move = split[:2]
        lastPosition_string, position_string = move.split("-")

        lastPosition, position = self.cipher(lastPosition_string), self.cipher(position_string)

        pieceTemp = None
        if piece_string == "R":
            pieceTemp = Modele.Elements.tour.Tour(lastPosition, self.numero_move%2 == 1)
            pieceTemp.moved = True
        elif piece_string == "K":
            pieceTemp = Modele.Elements.roi.Roi(lastPosition, self.numero_move%2 == 1)
            pieceTemp.moved = True
        elif piece_string == "Q":
            pieceTemp = Modele.Elements.reine.Reine(lastPosition, self.numero_move%2 == 1)
        elif piece_string == "N":
            pieceTemp = Modele.Elements.chevalier.Chevalier(lastPosition, self.numero_move%2 == 1)
        elif piece_string == "B":
            pieceTemp = Modele.Elements.fou.Fou(lastPosition, self.numero_move%2 == 1)
        elif piece_string == "P":
            pieceTemp = Modele.Elements.pion.Pion(lastPosition, self.numero_move%2 == 1)
            pieceTemp.first = False
            pieceTemp.second = False
        return [lastPosition, position, pieceTemp]

    #take a a1 and say it's position a1 -> [0,0]
    @staticmethod
    def cipher(string_position):
        return [ord(string_position[0]) - ord('a'), int(string_position[1]) - 1]

    # its meant to transform a move to a String (exemple) ->   "T:a1-b2" ou "P:e7-e8:Q" pour une _promotion
    @staticmethod
    def transform(position, lastPosition, piece, promotion):
        if isinstance(piece, Modele.Elements.roi.Roi):
            letter = 'K'
        elif isinstance(piece, Modele.Elements.reine.Reine):
            letter = 'Q'
        elif isinstance(piece, Modele.Elements.tour.Tour):
            letter = 'R'
        elif isinstance(piece, Modele.Elements.chevalier.Chevalier):
            letter = 'N'
        elif isinstance(piece, Modele.Elements.fou.Fou):
            letter = 'B'
        else:
            letter = 'P'

        letter_promotion = None

        if promotion is not None:
            print(promotion)
            if isinstance(promotion, Modele.Elements.roi.Roi):
                letter_promotion = 'K'
            elif isinstance(promotion, Modele.Elements.reine.Reine):
                letter_promotion = 'Q'
            elif isinstance(promotion, Modele.Elements.tour.Tour):
                letter_promotion = 'R'
            elif isinstance(promotion, Modele.Elements.chevalier.Chevalier):
                letter_promotion = 'N'
            elif isinstance(promotion, Modele.Elements.fou.Fou):
                letter_promotion = 'B'
            else:
                letter_promotion = 'P'


        return letter + ":" + chr(ord('a') + lastPosition[0]) + str(lastPosition[1] + 1) + "-" + chr(
            ord('a') + position[0]) + str(position[1] + 1) + ('' if promotion is None else ":" + letter_promotion)







