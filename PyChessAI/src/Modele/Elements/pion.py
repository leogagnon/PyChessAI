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
        '''
        C'est le constructeur qui va représenter un pion sur l'échiquier
        :param position: c'est la position que le chevalier occupe sur l'échiquier (c'est une position bidimensionnelle x et y qui peuvent prendre les valeurs entières de 0 à 7)
        :param couleurBlanc: c'est la couleur de la pièce (true -> elle est blanche ; False -> elle est noire)
        '''
        super().__init__(position, couleurBlanc, 1)
        self.first = True # True si le pion n'a pas encore bouger
        self.second = True # si le first est False et le que second est True sa vx dire que la piece peut se faire prendre en passant
        if couleurBlanc:
            self.vitesse = 1
        else:
            self.vitesse = -1
        self.choices = [TypePiece.REINE, TypePiece.TOUR, TypePiece.FOU, TypePiece.CAVALIER]

    # voir où sa se fait override (pieceM possibiliteBouger)
    def possibiliteBouger(self, board):
        '''
        Cette méthode a pour utilité de déterminer tous les mouvements que peut faire le pion (sans tenir compte si cela va mettre en danger le roi)
        :param board: C'est une matrice 8x8 qui contient toutes les pièces (les instances provenant du modèle) de l'échiquier
        :return: La méthode retourne une matrice booléenne 8x8 (c'est true où la pièce peut se déplacer)
        '''
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



    # pouvoir connaître les choix de __promotion possibles
    @staticmethod
    def getChoices():
        '''
        Donne tous les choix que le pion peut se faire promouvoir
        :return: une array qui contient tous ces choix
        '''
        return [TypePiece.REINE, TypePiece.TOUR, TypePiece.FOU, TypePiece.CAVALIER]
