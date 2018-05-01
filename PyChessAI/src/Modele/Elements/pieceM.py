# from abc import ABCMeta, abstractmethod pour rendre la classe en abstract
import Modele
from abc import ABC, abstractmethod
import Modele
from Modele.Game.enums import *


class PieceM(ABC):
    # constructeur
    def __init__(self, position, couleurBlanc, value):
        '''
        C'est une classe abstraite qui repréente une pièce d'un jeux d'échec normal (c'est à dire le pion, la tour, etc)
        :param position: c'est un array 2d de byte de 0 à 7
        :param couleurBlanc: c'est la couleur de la pièce (true -> blanc ; false -> noir)
        :param value: la valeur numérique d'une pièce (sa sera utile pour certain type d'évaluation pour les AI)
        '''
        self.position = position
        self.couleurBlanc = couleurBlanc
        self.value = value

    def testMouvementMemory(self, position, lastPosition, board):
        '''
        Faire le mouvement d'une pièce dans la mémoire de l'ordi (c'est à dire dans board) sans tenir compte de si c'est une move special (roque, prise en passant, etc)
        :param position: la position finale de la pièce qui veut se déplacer
        :param lastPosition: la position initiale de la pièce qui veut se déplacer
        :param board: une matrice 8x8 qui va contenir les pièces de l'échiquier
        '''
        board[position[0]][position[1]] = board[lastPosition[0]][lastPosition[1]]
        board[position[0]][position[1]].position = position
        board[lastPosition[0]][lastPosition[1]] = None

    # trouver la position du roi (en y entrant la couleur du roi)
    @staticmethod
    def trouverRoi(board, couleur):
        '''
        Sont utilité est de trouver la position du roi d'une certaine couleur (il ne peut y avoir plus d'un roi)
        :param board: une matrice 8x8 qui va contenir les pièces de l'échiquier
        :param couleur: la couleur du roi que nous cherchons
        :return: la position du roi
        '''
        cote = len(board)
        for i in range(cote):
            for j in range(cote):
                if isinstance(board[i][j], Modele.Elements.roi.Roi) and board[i][j].couleurBlanc == couleur:
                    return [i, j]
        return None

    # voir si la position qui est fournit est dans le grid
    def isInGame(self, position):
        '''
        Voir si la position est dans les délimitations de l'échiquier
        :param position: la position à vérifier sa délimitation
        :return: True -> si la position est une position valide dans les délimitations de l'échiquier False -> si ce n'est pas le cas
        '''
        cote = 7
        for i in range(2):
            if position[i] < 0 or position[i] > cote:
                return False
        return True

    # creer un tableau 2d 8x8 qui va montrer true pour les places ou la piece peut se déplacer
    @abstractmethod
    def possibiliteBouger(self, board):
        pass
