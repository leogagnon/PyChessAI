# from abc import ABCMeta, abstractmethod pour rendre la classe en abstract
import Modele
from abc import ABC, abstractmethod
import Modele
from Modele.Game.enums import *


class PieceM(ABC):
    # constructeur
    def __init__(self, position, couleurBlanc, value):
        self.position = position
        self.couleurBlanc = couleurBlanc
        self.value = value

    def testMouvementMemory(self, position, lastPosition, board):
        board[position[0]][position[1]] = board[lastPosition[0]][lastPosition[1]]
        board[position[0]][position[1]].position = position
        board[lastPosition[0]][lastPosition[1]] = None

    # trouver la position du roi (en y entrant la couleur du roi)
    @staticmethod
    def trouverRoi(board, couleur):
        cote = len(board)
        for i in range(cote):
            for j in range(cote):
                if isinstance(board[i][j], Modele.Elements.roi.Roi) and board[i][j].couleurBlanc == couleur:
                    return [i, j]
        return None

    # voir si la position qui est fournit est dans le grid
    def isInGame(self, position):
        cote = 7
        for i in range(2):
            if position[i] < 0 or position[i] > cote:
                return False
        return True

    # creer un tableau 2d 8x8 qui va montrer true pour les places ou la piece peut se déplacer
    @abstractmethod
    def possibiliteBouger(self, board):
        pass
