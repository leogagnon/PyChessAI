# from Modele.Elements.pieceM import PieceM
from Modele.Elements.tour import Tour
from Modele.Elements.reine import Reine
from Modele.Elements.fou import Fou
from Modele.Elements.chevalier import Chevalier
from Modele.Elements.pieceM import PieceM
from Modele.Game.enums import *


# la classe Chevalier est une PieceM de type chevalier (c'est à dire que c'est l'équivalent de la pièce chevalier pour la mémoire)
class Pion(PieceM):
    # constructeur
    def __init__(self, position, couleurBlanc):
        super().__init__(position, couleurBlanc, 1)
        self.first = True
        self.second = True
        if couleurBlanc:
            self.vitesse = 1
        else:
            self.vitesse = -1
        self.choices = [TypePiece.REINE, TypePiece.TOUR, TypePiece.FOU, TypePiece.CAVALIER]

    # voir où sa se fait override (pieceM possibiliteBouger)
    def possibiliteBouger(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        if board[self.position[0]][self.position[1] + self.vitesse] == None:
            moves[self.position[0]][self.position[1] + self.vitesse] = True
            if self.first:
                if board[self.position[0]][self.position[1] + self.vitesse * 2] == None:
                    moves[self.position[0]][self.position[1] + self.vitesse * 2] = True
        if self.position[0] + 1 <= 7:
            if board[self.position[0] + 1][self.position[1] + self.vitesse] != None and board[self.position[0] + 1][
                        self.position[1] + self.vitesse].couleurBlanc != self.couleurBlanc:
                moves[self.position[0] + 1][self.position[1] + self.vitesse] = True
            if isinstance(board[self.position[0] + 1][self.position[1]], Pion) and board[self.position[0] + 1][
                self.position[1]].couleurBlanc != self.couleurBlanc:
                if board[self.position[0] + 1][self.position[1]].second:
                    moves[self.position[0] + 1][self.position[1] + self.vitesse] = True
        if self.position[0] - 1 >= 0:
            if board[self.position[0] - 1][self.position[1] + self.vitesse] != None and board[self.position[0] - 1][
                        self.position[1] + self.vitesse].couleurBlanc != self.couleurBlanc:
                moves[self.position[0] - 1][self.position[1] + self.vitesse] = True
            if isinstance(board[self.position[0] - 1][self.position[1]], Pion) and board[self.position[0] - 1][
                self.position[1]].couleurBlanc != self.couleurBlanc:
                if board[self.position[0] - 1][self.position[1]].second:
                    moves[self.position[0] - 1][self.position[1] + self.vitesse] = True
        return moves

    # cette méthode fait en sorte de vérifier s'il y a vraiment une prise en passant par le pion et va faire le travail que mouvementMemory ne fait pas c'est à dire faire disparaitre le pion manger



    # pouvoir connaître les choix de promotion possibles
    @staticmethod
    def getChoices():
        return [TypePiece.REINE, TypePiece.TOUR, TypePiece.FOU, TypePiece.CAVALIER]
