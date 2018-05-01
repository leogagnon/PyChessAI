from Modele.Elements.pieceM import PieceM
#import Modele

#la classe Chevalier est une PieceM de type chevalier (c'est à dire que c'est l'équivalent de la pièce chevalier pour la mémoire)
class Tour(PieceM):
    #constructeur
    def __init__(self, position, couleurBlanc):
        '''
        C'est le constructeur qui va représenter une tour sur l'échiquier
        :param position: c'est la position que le chevalier occupe sur l'échiquier (c'est une position bidimensionnelle x et y qui peuvent prendre les valeurs entières de 0 à 7)
        :param couleurBlanc: c'est la couleur de la pièce (true -> elle est blanche ; False -> elle est noire)
        '''
        super().__init__(position, couleurBlanc, 5)
        self.moved = False

    # voir où sa se fait override (pieceM possibiliteBouger)
    def possibiliteBouger(self, board):
        '''
        Cette méthode a pour utilité de déterminer tous les mouvements que peut faire la tour (sans tenir compte si cela va mettre en danger le roi)
        :param board: C'est une matrice 8x8 qui contient toutes les pièces (les instances provenant du modèle) de l'échiquier
        :return: La méthode retourne une matrice booléenne 8x8 (c'est true où la pièce peut se déplacer)
        '''
        moves = [[False for _ in range(8)] for _ in range(8)]
        direction = [-1,1]
        test = []
        loop = False
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
                    
