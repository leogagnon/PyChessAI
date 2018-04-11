from Modele.Elements.pieceM import PieceM
from Modele.Game.enums import *
from Modele.Game.machine import Machine


class AlphaBeta(Machine):
    """Simple implémentation de l'algorithme alpha-bêta (Pour la documentation : https://fr.wikipedia.org/wiki/%C3%89lagage_alpha-b%C3%AAta )"""

    def play(self):
        """
        Voir méthode mère
        :return: Le meilleur move à faire
        """
        self.board = self.game.board
        self.position = None
        self.lastPosition = None
        self.__alphabeta_max(-300, 300, self.depth)

        return (self.lastPosition, self.position)

    def __init__(self, couleur, depth, game):
        self.board = None
        self.bestScore = -300
        self.depth = depth
        super().__init__(couleur, game)

        # Promotion fixé à reine
        self.promotion = TypePiece.REINE

    def __evaluate(self, board):
        """
        Évaluation sommaire de l'état d'un échiquier (c'est négatif si l'adversaire du Engines est en train de gagner et
        c'est positif si c'est le Engines qui gagne)
        :param board:
        :return:
        """
        total = 0
        for temp1 in board:
            for temp2 in temp1:
                if temp2 is not None:
                    multiplier = 1
                    if temp2.couleurBlanc != self.COULEUR_BLANC:
                        multiplier = -1
                    total += multiplier * temp2.value
                    total += multiplier * 0.1 * self.__nbr_de_moves(temp2.possibiliteBouger(board))
        return total

    def __nbr_de_moves(self, matrice):
        """
        Compte le nombre de True dans une matrice
        :param matrice: Ensembles des moves possibles pour une pièce
        :return: Nombres de coups possibles
        """
        total = 0
        for i in matrice:
            total += sum(i)
        return total

    def __alphabeta_min(self, alpha, beta, depthleft):

        # Si c'est au bout du "decision tree" sortir l'évaluation de l'environnement
        if depthleft == 0:
            return self.__evaluate(self.board)

        # Voir si le roi adverse est en échec et mat (le score est très haut pcq c'est la meilleur possibilité pour vous -> à prioritiser)
        posRoi = PieceM.trouverRoi(self.board, not self.COULEUR_BLANC)
        if self.board[posRoi[0]][posRoi[1]].mat(self.board):
            return 300

        # Faire chaqu'un des moves possibles et récursivement y chercher une évaluation
        for temp1 in self.board:
            for temp2 in temp1:
                if temp2 is not None and temp2.couleurBlanc != self.COULEUR_BLANC:
                    moves = temp2.possibiliteBouger(self.board)
                    self.board[posRoi[0]][posRoi[1]].acceptableMove(moves, self.board, temp2.position)

                    initial = temp2.position[:]
                    for i in range(len(moves)):
                        for j in range(len(moves[i])):
                            if moves[i][j]:

                                # Faire le mouvement
                                self.game.move([i, j], initial)
                                # Evaluer
                                score = self.__alphabeta_max(alpha, beta, depthleft - 1)
                                # Undo
                                self.game.undo()

                                if score <= alpha:
                                    return alpha
                                if score < beta:
                                    beta = score

        return beta

    def __alphabeta_max(self, alpha, beta, depthleft):
        if depthleft == 0:
            return self.__evaluate(self.board)
        posRoi = PieceM.trouverRoi(self.board, self.COULEUR_BLANC)
        if self.board[posRoi[0]][posRoi[1]].mat(self.board):
            return -300

        for temp1 in self.board:
            for temp2 in temp1:
                if temp2 is not None and temp2.couleurBlanc == self.COULEUR_BLANC:
                    moves = temp2.possibiliteBouger(self.board)
                    self.board[posRoi[0]][posRoi[1]].acceptableMove(moves, self.board, temp2.position)

                    initial = temp2.position[:]
                    for i in range(len(moves)):
                        for j in range(len(moves[i])):
                            if moves[i][j]:
                                self.game.move([i, j], initial)
                                score = self.__alphabeta_min(alpha, beta, depthleft - 1)
                                self.game.undo()

                                if depthleft == self.depth:
                                    if (self.position is not None and score > self.bestScore) or self.position is None:
                                        # sauvegarder le mouvement optimal pour l'instant (à la fin de la récursion c'est ces donnés qui vont être utilisé pour faire le mouvement du Engines)
                                        self.position = [i, j]
                                        self.lastPosition = initial
                                        self.bestScore = score

                                if score >= beta:
                                    return beta
                                if score > alpha:
                                    alpha = score
        return alpha
