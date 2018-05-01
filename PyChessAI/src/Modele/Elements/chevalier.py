from Modele.Elements.pieceM import PieceM


#la classe Chevalier est une PieceM de type chevalier (c'est à dire que c'est l'équivalent de la pièce chevalier pour la mémoire)
class Chevalier(PieceM):
    #le constructeur
    def __init__(self, position, couleurBlanc):
        '''
        C'est le constructeur qui va représenter un chevalier sur l'échiquier
        :param position: c'est la position que le chevalier occupe sur l'échiquier (c'est une position bidimensionnelle x et y qui peuvent prendre les valeurs entières de 0 à 7)
        :param couleurBlanc: c'est la couleur de la pièce (true -> elle est blanche ; False -> elle est noire)
        '''
        super().__init__(position, couleurBlanc, 3)

    #voir où sa se fait override (pieceM possibiliteBouger)
    def possibiliteBouger(self, board):
        '''
        Cette méthode a pour utilité de déterminer tous les mouvements que peut faire le chevalier (sans tenir compte si cela va mettre en danger le roi)
        :param board: C'est une matrice 8x8 qui continent toutes les pièces (les instances provenant du modèle) de l'échiquier
        :return: La méthode retourne une matrice booléenne 8x8 (c'est true où la pièce peut se déplacer)
        '''
        chevMoves =  [[1,2],[2,1],[2,-1],[1,-2],[-1,2],[-2,1],[-2,-1],[-1,-2]]
        moves = [[False for _ in range(8)] for _ in range(8)]
        for possibilities in chevMoves:
            test = [possibilities[0] + self.position[0], possibilities[1] + self.position[1]]
            if(self.isInGame(test)):
                if board[test[0]][test[1]] == None or board[test[0]][test[1]].couleurBlanc != self.couleurBlanc:
                    moves[test[0]][test[1]] = True
        return moves
