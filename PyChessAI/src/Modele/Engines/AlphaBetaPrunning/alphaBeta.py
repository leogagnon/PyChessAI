from Modele.Game.machine import Machine
from Modele.Elements.pieceM import PieceM
from Modele.Game.enums import *


# Simple implémentation de l'algorithme alpha-bêta (Pour la documentation : https://fr.wikipedia.org/wiki/%C3%89lagage_alpha-b%C3%AAta )

class AlphaBeta(Machine):
    def __init__(self, couleur, depth, game):
        self.board = None
        self.bestScore = -300
        self.depth = depth
        super().__init__(couleur, game)

        # Promotion fixé à reine
        self.promotion = TypePiece.REINE

    def evaluate(self, board):
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
                    total += multiplier * 0.1 * self.nbr_true(temp2.possibiliteBouger(board))
        return total

    def nbr_true(self, matrice):
        """
        Compte le nombre de True dans une matrice
        :param matrice: Ensembles des moves possibles pour une pièce
        :return: Nombres de coups possibles
        """
        total = 0
        for i in matrice:
            total += sum(i)
        return total

    # play needs to call alphaBeta (since this is the Engines in this case)
    def play(self):
        """
        Voir méthode mère
        :return: Le meilleur move à faire
        """
        self.board = self.game.board
        self.position = None
        self.lastPosition = None
        self.alphaBetaMax(-300, 300, self.depth)

        return (self.lastPosition, self.position)

    # Pour comprendre cela, il faut comprendre comment alphaBeta fonctionne, mais si vous vous êtes documenté c'est l'équivalent de ce l'adversaire pourrait jouer

    def alphaBetaMin(self, alpha, beta, depthleft):

        # Si c'est au bout du "decision tree" sortir l'évaluation de l'environnement
        if depthleft == 0:
            return self.evaluate(self.board)

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
                                score = self.alphaBetaMax(alpha, beta, depthleft - 1)
                                # Undo
                                self.game.undo()

                                if score <= alpha:
                                    return alpha
                                if score < beta:
                                    beta = score

        return beta

    # Pour comprendre cela, il faut comprendre comment alphaBeta fonctionne, mais si vous vous êtes documenté c'est l'équivalent de vous (qui essayer de maximiser votre "score")
    # Pour comprendre les parties de code voir la méthode au-dessus c'est approximativement la même chose

    def alphaBetaMax(self, alpha, beta, depthleft):
        if depthleft == 0:
            return self.evaluate(self.board)
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
                                score = self.alphaBetaMin(alpha, beta, depthleft - 1)
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
