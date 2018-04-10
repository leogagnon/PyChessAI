from Modele.Game.machine import Machine
from Modele.Elements.memoire import Memoire
from Modele.Game.enums import *
from Modele.AI.ucip import UCIP


class LCZero(Machine):
    def __init__(self, couleur, memoire):
        self.lczero = UCIP(command=['Modele/AI/LeelaChessZero/lczeroEngine','-w','Modele/AI/LeelaChessZero/weights.txt'])
        self.promotion = None
        super().__init__(couleur, memoire)

    def play(self, board):
            self.lczero.set_position(self.get_liste_moves(self.memoire.tous_move))
            best_move = self.lczero.get_best_move()
            best_move = self.check_promotion(best_move)
            self.lastPosition = Memoire.cipher(best_move[:2])
            self.position = Memoire.cipher(best_move[-2:])

            return (self.lastPosition, self.position)


    def get_liste_moves(self, tous_moves):
        """
        Transforme la liste de coup de Mémoire en tableau de String -> ex. ['e2e4', 'e7e6']
        :return: La liste de coups
        """
        liste_moves = []

        for i in tous_moves:
            split = i.split(':')
            temp = i.split(':')[1].split('-')
            move = temp[0] + temp[1]
            if len(split) == 3:
                move += split[2].lower()
            liste_moves.append(move)

        return liste_moves

    def check_promotion(self, move):
        if len(move) == 5:
            choix = move[4]

            if choix == 'q':
                self.promotion = TypePiece.REINE
            elif choix == 'r':
                self.promotion = TypePiece.TOUR
            elif choix == 'b':
                self.promotion = TypePiece.FOU
            elif choix == 'n':
                self.promotion = TypePiece.CAVALIER
        return move[:4]

