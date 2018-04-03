from Modele.Game.machine import Machine
from Modele.Elements.memoire import Memoire
import Modele
from Modele.AI.ucip import UCIP


class LCZero(Machine):
    def __init__(self, couleur):
        self.lczero = UCIP(command=['Modele/AI/LeelaChessZero/lczeroEngine','-w','Modele/AI/LeelaChessZero/weights.txt'])
        super().__init__(couleur)

    def play(self, board, tous_moves):
            self.lczero.set_position(self.get_liste_moves(tous_moves))
            best_move = self.lczero.get_best_move()

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
            temp = i.split(':')[1].split('-')
            move = temp[0] + temp[1]
            liste_moves.append(move)

        return liste_moves