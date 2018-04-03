import Modele
from Modele.Game.enums import *


#cette classe est utile pour undo (ce qui sera utile dans chaque mode_de_jeu)
#les deux méthode qui vont être utile en dehors de la classe sont move_made et undo


class Memoire:

    def __init__(self):
        self.memoireSpecial = []  # conserve [le # du move special, le numero_move]
        self.memoireManger = []  # conserve [la pièce mangé, le numero_move]
        self.numero_move = 0
        self.tous_move = []  # va n'être qu'un array de String qui va conserver toute les informations de quelle pièce a bouger de où à où

    # !!! c'est important d'appeler cette méthode pour pouvoir avoir la capacité de undo
    def move_made(self,position, lastPosition, piece, manger, special):
        self.normal(position, lastPosition, piece)
        if special != MoveSpecial.NULL:
            self.special(special)
        if manger is not None:
            self.mange(manger)
        self.numero_move += 1

    #normal means that it only saves what piece moved from where to where
    def normal(self, position, lastPosition, piece):
        self.tous_move.append(Memoire.transform(position, lastPosition, piece))

    #saves a eaten piece
    def mange(self, piece):
        self.memoireManger.append([piece, self.numero_move])
    #saves a special moves (roque, prise en passant et promotion)
    def special(self, special):
        self.memoireSpecial.append([special, self.numero_move])
    #faire le changement dans la matrice board qui défait le dernier move fait

    def undo(self, board):

        informations = self.undo_transform(self.tous_move.pop()) #lastPosition, position, piece qui a été bouger
        lastPosition, position, pieceBouger = informations[0], informations[1], informations[2]

        tempPiece = None
        if len(self.memoireManger) != 0 and self.memoireManger[-1][1] == self.numero_move - 1:
            tempPiece = self.memoireManger.pop()[0]
        board[position[0]][position[1]] = tempPiece
        board[lastPosition[0]][lastPosition[1]] = pieceBouger
        board[lastPosition[0]][lastPosition[1]].position = lastPosition[:]

        if len(self.memoireSpecial) != 0 and self.memoireSpecial[-1][1] == self.numero_move - 1:
            special = self.memoireSpecial.pop()[0]
            if special == MoveSpecial.PRISE_EN_PASSANT:#prise en passant
                board[position[0]][lastPosition[1]] = Modele.Elements.pion.Pion([position[0], lastPosition[1]], not pieceBouger.couleurBlanc)
                board[position[0]][lastPosition[1]].first = False
            elif special == MoveSpecial.PROMOTION: # promotion
                board[lastPosition[0]][lastPosition[1]] = Modele.Elements.pion.Pion(lastPosition, pieceBouger.couleurBlanc)
                board[lastPosition[0]][lastPosition[1]].first = False
                board[lastPosition[0]][lastPosition[1]].second = False
            elif special == MoveSpecial.ROQUE:#roque
                board[lastPosition[0]][lastPosition[1]].moved = False
                if position[0] == 6:
                    board[7][position[1]] = Modele.Elements.tour.Tour([7,position[1]], pieceBouger.couleurBlanc)
                    board[5][position[1]] = None
                else:
                    board[0][position[1]] = Modele.Elements.tour.Tour([0,position[1]], pieceBouger.couleurBlanc)
                    board[3][position[1]] = None
            elif special == MoveSpecial.PREMIER_MOUVEMENT_TOUR: #the rook has been moved for the first time
                board[lastPosition[0]][lastPosition[1]].moved = False
            elif special == MoveSpecial.PREMIER_MOUVEMENT_ROI: #the king has been moved for the first time and did not do the roque
                board[lastPosition[0]][lastPosition[1]].moved = False
            elif special == MoveSpecial.PREMIER_MOUVEMENT_PION: #first move of the pawn
                board[lastPosition[0]][lastPosition[1]].first = True
                board[lastPosition[0]][lastPosition[1]].second = True
            elif special == MoveSpecial.PRISE_EN_PASSANT_IMPOSSIBLE: #the pawn could do his second move
                board[lastPosition[0]][lastPosition[1]].second = True
        self.numero_move -= 1

    #prendre le string qui a été noté et output le move qui a été fait et avec quelle pièce
    def undo_transform(self, string_move):
        piece_string, move = string_move.split(":")
        lastPosition_string, position_string = move.split("-")

        lastPosition, position = self.cipher(lastPosition_string), self.cipher(position_string)

        pieceTemp = None
        if piece_string == "T":
            pieceTemp = Modele.Elements.tour.Tour(lastPosition, self.numero_move%2 == 1)
            pieceTemp.moved = True
        elif piece_string == "R":
            pieceTemp = Modele.Elements.roi.Roi(lastPosition, self.numero_move%2 == 1)
            pieceTemp.moved = True
        elif piece_string == "D":
            pieceTemp = Modele.Elements.reine.Reine(lastPosition, self.numero_move%2 == 1)
        elif piece_string == "C":
            pieceTemp = Modele.Elements.chevalier.Chevalier(lastPosition, self.numero_move%2 == 1)
        elif piece_string == "F":
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

    # its meant to transform a move to a String (exemple) ->   "T:a1-b2"
    @staticmethod
    def transform(position, lastPosition, piece):
        letter = ' '
        if isinstance(piece, Modele.Elements.roi.Roi):
            letter = 'R'
        elif isinstance(piece, Modele.Elements.reine.Reine):
            letter = 'D'
        elif isinstance(piece, Modele.Elements.tour.Tour):
            letter = 'T'
        elif isinstance(piece, Modele.Elements.chevalier.Chevalier):
            letter = 'C'
        elif isinstance(piece, Modele.Elements.fou.Fou):
            letter = 'F'
        else:
            letter = 'P'
        return letter + ":" + chr(ord('a') + lastPosition[0]) + str(lastPosition[1] + 1) + "-" + chr(
            ord('a') + position[0]) + str(position[1] + 1)







