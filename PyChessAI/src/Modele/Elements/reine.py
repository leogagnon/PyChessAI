from Modele.Elements.pieceM import PieceM
#la classe Chevalier est une PieceM de type chevalier (c'est à dire que c'est l'équivalent de la pièce chevalier pour la mémoire)
class Reine(PieceM):

    #constructeur
    def __init__(self, position, couleurBlanc):
        super().__init__(position, couleurBlanc, 9)

    # voir où sa se fait override (pieceM possibiliteBouger)
    def possibiliteBouger(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        #copy coller partie fou
        direction = [-1, 1]
        test = []
        for i in direction:
            for j in direction:
                test = self.position[:]
                loop = True
                
                while loop:
                    test[0] += i
                    test[1] += j
                    if self.isInGame(test):
                        if board[test[0]][test[1]] == None:
                            moves[test[0]][test[1]] = True
                        elif board[test[0]][test[1]].couleurBlanc == self.couleurBlanc:
                            loop = False
                        else:
                            moves[test[0]][test[1]] = True
                            loop = False
                    else:
                        loop = False

        #copy coller de partie Tour
        for temp in direction:
            test = self.position[:]
            loop = True

            while loop:
                test[0] += temp
                if self.isInGame(test):
                    if board[test[0]][test[1]] == None:
                        moves[test[0]][test[1]] = True
                    elif board[test[0]][test[1]].couleurBlanc == self.couleurBlanc:
                        loop = False
                    else:
                        moves[test[0]][test[1]] = True
                        loop = False
                else:
                    loop = False

        for temp2 in direction:
            test = self.position[:]
            loop = True
            while loop:
                test[1] += temp2
                if self.isInGame(test):
                    if board[test[0]][test[1]] == None:
                        moves[test[0]][test[1]] = True
                    elif board[test[0]][test[1]].couleurBlanc == self.couleurBlanc:
                        loop = False
                    else:
                        moves[test[0]][test[1]] = True
                        loop = False
                else:
                    loop = False
        return moves
