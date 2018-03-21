from Modele.Elements.pieceM import PieceM


#la classe Chevalier est une PieceM de type chevalier (c'est à dire que c'est l'équivalent de la pièce chevalier pour la mémoire)
class Chevalier(PieceM):
    #le constructeur
    def __init__(self, position, couleurBlanc):
        super().__init__(position, couleurBlanc, 3)

    #voir où sa se fait override (pieceM possibiliteBouger)
    def possibiliteBouger(self, board):
        chevMoves =  [[1,2],[2,1],[2,-1],[1,-2],[-1,2],[-2,1],[-2,-1],[-1,-2]]
        moves = [[False for _ in range(8)] for _ in range(8)]
        for possibilities in chevMoves:
            test = [possibilities[0] + self.position[0], possibilities[1] + self.position[1]]
            if(self.isInGame(test)):
                if board[test[0]][test[1]] == None or board[test[0]][test[1]].couleurBlanc != self.couleurBlanc:
                    moves[test[0]][test[1]] = True
        return moves
