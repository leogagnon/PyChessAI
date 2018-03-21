#from abc import ABCMeta, abstractmethod pour rendre la classe en abstract
import Modele
from abc import ABC, abstractmethod
import Modele
from Modele.Players.enums import *

class PieceM(ABC):
    #constructeur
    def __init__(self, position, couleurBlanc, value):
        self.position = position
        self.couleurBlanc = couleurBlanc
        self.value = value

    
    #faire un changement dans le board (déplacement normal dans la mémoire de l'ordi) 
    def testMouvementMemory(self, position, lastPosition, board):
        board[position[0]][position[1]] = board[lastPosition[0]][lastPosition[1]]
        board[position[0]][position[1]].position = position
        board[lastPosition[0]][lastPosition[1]] = None
    
    #trouver la position du roi (en y entrant la couleur du roi)
    @staticmethod
    def trouverRoi(board, couleur):
        cote = len(board)
        for i in range(cote):
            for j in range(cote):
                if isinstance(board[i][j], Modele.Elements.roi.Roi) and board[i][j].couleurBlanc == couleur:
                    return [i,j]
        return None
    
    #voir si la position qui est fournit est dans le grid
    def isInGame(self, position):
        cote = 7
        for i in range(2):
            if position[i] < 0 or position[i] > cote:
                return False
        return True

    #va faire le changement plus complet que testMouvementMemory dans le sens ou il va tenir en compte de savoir s'il y a un coup special
    def mouvementMemory(self, position, lastPosition, board):
        special = MoveSpecial.NULL
        if isinstance(board[lastPosition[0]][lastPosition[1]], Modele.Elements.pion.Pion):
            temp = board[lastPosition[0]][lastPosition[1]].ongoingPassant(position, lastPosition, board)
            if temp:
                special = MoveSpecial.PRISE_EN_PASSANT
        self.testMouvementMemory(position, lastPosition, board)
        if isinstance(board[position[0]][position[1]], Modele.Elements.pion.Pion):
            if board[position[0]][position[1]].first:
                special = MoveSpecial.PREMIER_MOUVEMENT_PION
            elif board[position[0]][position[1]].second:
                special = MoveSpecial.PRISE_EN_PASSANT_IMPOSSIBLE
        board[position[0]][position[1]].prisePassant(lastPosition, board)

        if isinstance(board[position[0]][position[1]], Modele.Elements.pion.Pion):
            if position[1] == 7 or position[1] == 0:
                output = Modele.Players.opponents.Opponents.getPlayerTour().choixPromotion(None, None)
                board[position[0]][position[1]].promotion(output, board)
                special = MoveSpecial.PROMOTION
        elif isinstance(board[position[0]][position[1]], Modele.Elements.tour.Tour):
            if not(board[position[0]][position[1]].moved):
                board[position[0]][position[1]].moved = True
                special = MoveSpecial.MOUVEMENT_TOUR
        elif isinstance(board[position[0]][position[1]], Modele.Elements.roi.Roi):
            if not board[position[0]][position[1]].moved:
                special = MoveSpecial.PREMIER_MOUVEMENT_ROI
                if lastPosition[0] - position[0] == -2 :
                    board[7][position[1]].mouvementMemory([position[0] -1, position[1]], [7, position[1]], board)
                    special = MoveSpecial.ROQUE
                elif lastPosition[0] - position[0] == 2 :
                    board[0][position[1]].mouvementMemory([position[0] +1, position[1]], [0, position[1]], board)
                    special = MoveSpecial.ROQUE
                board[position[0]][position[1]].moved = True
        return special
    #va être à faire passer pour chaque tour
    def prisePassant(self, lastPosition, board):
        if isinstance(board[self.position[0]][self.position[1]], Modele.Elements.pion.Pion):
            if board[self.position[0]][self.position[1]].first:
                for temp in board:
                    for temp2 in temp:
                        if isinstance(temp2, Modele.Elements.pion.Pion) and temp2.second:
                            temp2.second = False
                board[self.position[0]][self.position[1]].first = False
                if abs(lastPosition[1] - self.position[1]) == 2:
                    board[self.position[0]][self.position[1]].second = True
            elif board[self.position[0]][self.position[1]].second:
                board[self.position[0]][self.position[1]].second = False
        else:
            for temp in board:
                for temp2 in temp:
                    if isinstance(temp2, Modele.Elements.pion.Pion) and temp2.second:
                        temp2.second = False

    # creer un tableau 2d 8x8 qui va montrer true pour les places ou la piece peut se déplacer
    @abstractmethod
    def possibiliteBouger(self, board):
        pass



        
