from Modele.Game.machine import Machine
from Modele.Elements.memoire import Memoire
from Modele.Elements.pion import Pion
from Modele.AI.ucip import UCIP
from Modele.Game.enums import *


class Stockfish(Machine):
    def __init__(self, couleur, depth):
        self.stockfish = UCIP(command=['Modele/AI/Stockfish9/stockfish9Engine'], depth=depth)
        super().__init__(couleur)

    def play(self, board, memoire):
        self.stockfish.set_position(self.get_liste_moves(memoire.tous_move))
        best_move = self.stockfish.get_best_move()
        best_move = best_move[:4]

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


