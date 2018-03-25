#from Modele.Elements.pieceM import PieceM
from Modele.Elements.tour import Tour
from Modele.Elements.reine import Reine
from Modele.Elements.fou import Fou
from Modele.Elements.chevalier import Chevalier
from Modele.Elements.pieceM import PieceM
from Modele.Players.enums import *

#la classe Chevalier est une PieceM de type chevalier (c'est à dire que c'est l'équivalent de la pièce chevalier pour la mémoire)
class Pion(PieceM):

    #constructeur
    def __init__(self, position, couleurBlanc):
        super().__init__(position, couleurBlanc, 1)
        self.first = True
        self.second = True
        if couleurBlanc:
            self.vitesse = 1
        else:
            self.vitesse = -1
        self.choices = [TypePiece.REINE, TypePiece.TOUR, TypePiece.FOU, TypePiece.CAVALIER]
        
    #c'est pour savoir si le pion est dans une self.position faible (pour l'évaluation chez le comp)
    def disadvantage(self, board):
        if board[self.position[0]][self.position[1] + self.vitesse] != None and board[self.position[0]][self.position[1] + self.vitesse].couleurBlanc != self.couleurBlanc:
            return True
        y = self.position[1] + self.vitesse
        continu = True
        while continu:
            if (y <= 6 and self.couleurBlanc) or (y >= 1 and not self.couleurBlanc):
                continu = False
            elif continu and isinstance(board[self.position[0]][y], Pion) and board[self.position[1]][y].couleurBlanc:
                return True
            y += self.vitesse
        return False

    # voir où sa se fait override (pieceM possibiliteBouger)
    def possibiliteBouger(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        if board[self.position[0]][self.position[1] + self.vitesse] == None:
            moves[self.position[0]][self.position[1] + self.vitesse] = True
            if self.first:
                if board[self.position[0]][self.position[1] + self.vitesse*2] == None:
                    moves[self.position[0]][self.position[1] + self.vitesse*2] = True
        if self.position[0] + 1 <= 7:
            if board[self.position[0] + 1][self.position[1] + self.vitesse] != None and board[self.position[0] + 1][self.position[1] + self.vitesse].couleurBlanc != self.couleurBlanc:
                moves[self.position[0] + 1][self.position[1] + self.vitesse] = True
            if isinstance(board[self.position[0] + 1][self.position[1]], Pion) and board[self.position[0] + 1][self.position[1]].couleurBlanc != self.couleurBlanc:
                if board[self.position[0]+1][self.position[1]].second:
                    moves[self.position[0] + 1][self.position[1] + self.vitesse] = True
        if self.position[0] - 1 >= 0:
            if board[self.position[0] - 1][self.position[1] + self.vitesse] != None and board[self.position[0] - 1][self.position[1] + self.vitesse].couleurBlanc != self.couleurBlanc:
                moves[self.position[0] - 1][self.position[1] + self.vitesse] = True
            if isinstance(board[self.position[0] - 1][self.position[1]], Pion) and board[self.position[0] - 1][self.position[1]].couleurBlanc != self.couleurBlanc:
                if board[self.position[0]-1][self.position[1]].second:
                    moves[self.position[0]-1][self.position[1] + self.vitesse] = True
        return moves

    #cette méthode fait en sorte de vérifier s'il y a vraiment une prise en passant par le pion et va faire le travail que mouvementMemory ne fait pas c'est à dire faire disparaitre le pion manger
    def ongoingPassant(self, position, lastPosition, board):
        if abs(position[0] - lastPosition[0]) == 1 and board[position[0]][position[1]] == None:
            board[position[0]][lastPosition[1]] = None
            return True
        return False

    #si le pion atteint la rangé de la fin faire une promotion
    def promotion(self, entree, board):
        tempPieceM = None
        test = self.position[:]
        if (entree == self.choices[0]):
            tempPieceM = Reine(test, board[test[0]][test[1]].couleurBlanc)
        elif entree == self.choices[1]:
            tempPieceM = Tour(test, board[test[0]][test[1]].couleurBlanc)
        elif entree == self.choices[2]:
            tempPieceM = Fou(test, board[test[0]][test[1]].couleurBlanc)
        elif entree == self.choices[3]:
            tempPieceM = Chevalier(test, board[test[0]][test[1]].couleurBlanc)
        board[self.position[0]][self.position[1]] = tempPieceM
        return tempPieceM

    #pouvoir connaître les choix de promotion possibles
    @staticmethod
    def getChoices():
        return [TypePiece.REINE, TypePiece.TOUR, TypePiece.FOU, TypePiece.CAVALIER]
            
