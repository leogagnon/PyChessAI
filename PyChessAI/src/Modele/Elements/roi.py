from Modele.Elements.pieceM import PieceM
from Modele.Elements.tour import Tour
import Modele


# la classe Chevalier est une PieceM de type chevalier (c'est à dire que c'est l'équivalent de la pièce chevalier pour la mémoire)
class Roi(PieceM):
    # constructeur
    def __init__(self, position, couleurBlanc):
        '''
        C'est le constructeur qui va représenter un roi sur l'échiquier
        :param position: c'est la position que le chevalier occupe sur l'échiquier (c'est une position bidimensionnelle x et y qui peuvent prendre les valeurs entières de 0 à 7)
        :param couleurBlanc: c'est la couleur de la pièce (true -> elle est blanche ; False -> elle est noire)
        '''
        super().__init__(position, couleurBlanc, 200)
        self.moved = False

    # voir où sa se fait override (pieceM possibiliteBouger)
    def possibiliteBouger(self, board):
        '''
        Cette méthode a pour utilité de déterminer tous les mouvements que peut faire le roi (sans tenir compte si cela va mettre en danger le roi)
        :param board: C'est une matrice 8x8 qui contient toutes les pièces (les instances provenant du modèle) de l'échiquier
        :return: La méthode retourne une matrice booléenne 8x8 (c'est true où la pièce peut se déplacer)
        '''
        moves = [[False for _ in range(8)] for _ in range(8)]
        direction = [-1, 0, 1]
        test = []

        for i in direction:
            for j in direction:
                if i != 0 or j != 0:
                    test = [self.position[0] + i, self.position[1] + j]
                    if self.isInGame(test):
                        if board[test[0]][test[1]] == None:
                            moves[test[0]][test[1]] = True
                            if j == 0 and not self.moved:
                                test = [self.position[0] + i * 2, self.position[1]]
                                if board[test[0]][test[1]] == None:
                                    if i < 0 and board[test[0] - 1][test[1]] == None and isinstance(
                                            board[0][self.position[1]], Tour) and not board[0][self.position[1]].moved:
                                        moves[test[0]][test[1]] = True
                                    elif i > 0 and isinstance(board[7][self.position[1]], Tour) and not board[7][
                                        self.position[1]].moved:
                                        moves[test[0]][test[1]] = True
                        elif board[test[0]][test[1]].couleurBlanc != self.couleurBlanc:
                            moves[test[0]][test[1]] = True
        return moves

    # Voir toutes les places qui sont touchés par un adversaire
    # Va être essentiel pour la méthode echec dans la classe Roi
    def opponentMoves(self, board):
        '''
        Va donner une matrice booléenne 8x8 qui va représenter toutes les positions qui sont accessibles par les adversaires (True -> accessible ; False -> pas accessible)
        :param board: une matrice 8x8 qui va contenir les pièces de l'échiquier
        :return: la matrice booléenne 8x8 qui va contenir les positions accessibles par l'équipe adverse
        '''
        moves = [[False for _ in range(8)] for _ in range(8)]

        for temp in board:
            for temp2 in temp:
                if temp2 != None and temp2.couleurBlanc != self.couleurBlanc:
                    adder = temp2.possibiliteBouger(board)
                    for i in range(len(adder)):
                        for j in range(len(adder[i])):
                            if adder[i][j] and not moves[i][j]:
                                moves[i][j] = True

        return moves

    # Voir si votre roi est en état d'échec
    def echec(self, board, couleurBlanc):
        '''
        Voir si notre roi est en échec
        :param board: la matrice 8x8 qui contient les pièces de l'échiquier
        :param couleurBlanc: la couleur du roi que vous voulez voir s'il est en échec
        :return: Valeur booléenne -> si c'est en échec
        '''
        positionRoi = PieceM.trouverRoi(board, couleurBlanc)
        others = self.opponentMoves(board)
        if others[positionRoi[0]][positionRoi[1]]:
            return True
        return False

    # voir si un move est acceptable (c'est-à dire est ce qu'en bougeant cela va faire en sorte qu'un roi qui n'est pas mat se mette en état d'échec)
    def acceptableMove(self, moves, board, position):
        '''
        Changer la matrice moves pour tenir compte de la légalité du move (si le mouvement met le roi en échec)
        :param moves: une matrice booléenne 8x8 qui représente où c'est légal de se déplacer
        :param board: une matrice 8x8 qui contient toutes les pièces de l'échiquier
        :param position: la position initiale de la pièce qui veut se déplacer
        '''
        initial = position[:]
        # regarde à travers tout les moves possibles
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                if moves[i][j]:#le move est possible
                    if board[i][j] != None: #il y a une pièce sur la case
                        erasedPiece = board[i][j]
                        self.testMouvementMemory([i, j], initial, board)
                        if self.echec(board, self.couleurBlanc):
                            moves[i][j] = False
                        self.testMouvementMemory(initial, [i, j], board)
                        board[i][j] = erasedPiece
                    else:
                        if isinstance(board[initial[0]][initial[1]], Modele.Elements.roi.Roi) and initial[0] == 4: # c'est une tentative de roque
                            if moves[initial[0] + 2][initial[1]]:  #voir si le roque à droite est légal
                                if self.echec(board, self.couleurBlanc):
                                    moves[initial[0] + 2][initial[1]] = False
                                elif not moves[initial[0] + 1][initial[1]]:
                                    moves[initial[0] + 2][initial[1]] = False
                            elif moves[initial[0] - 2][initial[1]]: #voir si le roque à gauche est légal
                                if self.echec(board, self.couleurBlanc): # si le roi est en échec il ne peut pas faire le roque
                                    moves[initial[0] - 2][initial[1]] = False
                                else:
                                    self.testMouvementMemory([initial[0] - 1, initial[1]], initial, board)
                                    if self.echec(board, self.couleurBlanc):
                                        moves[initial[0] - 1][initial[1]] = False
                                    self.testMouvementMemory(initial, [initial[0] - 1, initial[1]], board)
                                    if not moves[initial[0] - 1][initial[1]]:
                                        moves[initial[0] - 2][initial[1]] = False
                        self.testMouvementMemory([i, j], initial, board)
                        if self.echec(board, self.couleurBlanc):
                            moves[i][j] = False
                        self.testMouvementMemory(initial, [i, j], board)

    # voir si une pièce peut au moins faire un move (utile pour la méthode mat)
    def onlyLegal(self, moves):
        '''
        Voir si la matrice moves a au moins un move possible
        :param moves: C'est une matrice booléenne 8x8 qui représente toutes les positions qu'une pièce peut bouger  si true -> peut bouger else ne peut pas
        :return: Si la pièce peut au moins bouger à une place
        '''
        taille = 8
        for i in range(taille):
            for j in range(taille):
                if moves[i][j]:
                    return True
        return False

    # voir si le roi est en échec et mat
    def mat(self, board):
        '''
        Voir si le roi est en mat
        :param board: C'est une matrice 8x8 qui contient toutes les pièces de l'échiquier
        :return: True -> le roi est matté False -> le roi n'est pas en échec et mat
        '''
        if not self.echec(board, self.couleurBlanc):
            return False

        for temp1 in board:
            for temp2 in temp1:
                if temp2 != None and temp2.couleurBlanc == self.couleurBlanc:
                    moves = temp2.possibiliteBouger(board)
                    self.acceptableMove(moves, board, temp2.position[:])
                    if self.onlyLegal(moves):
                        return False

        return True
