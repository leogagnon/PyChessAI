from Modele.Game.machine import Machine
from Modele.Elements.memoire import Memoire
import Modele
from Modele.AI.ucip import UCIP


class Stockfish(Machine):
    def __init__(self, couleur, depth):
        self.stockfish = UCIP(command=['Modele/AI/Stockfish9/stockfish_9_x64'], depth=depth)
        super().__init__(couleur)

    def play(self, board):
        self.stockfish.set_position(self.get_liste_moves())
        best_move = self.stockfish.get_best_move()

        self.lastPosition = Memoire.cipher(best_move[:2])
        self.position = Memoire.cipher(best_move[-2:])

        pieceTemp = board[self.position[0]][self.position[1]]
        special = board[self.lastPosition[0]][self.lastPosition[1]].mouvementMemory(self.position, self.lastPosition,
                                                                                    board)
        Modele.Elements.memoire.Memoire.move_made(self.position, self.lastPosition,
                                                  board[self.position[0]][self.position[1]], pieceTemp, special)

    def get_liste_moves(self):
        """
        Transforme la liste de coup de Mémoire en tableau de String -> ex. ['e2e4', 'e7e6']
        :return: La liste de coups
        """
        liste_moves = []

        for i in Memoire.tous_move:
            temp = i.split(':')[1].split('-')
            move = temp[0] + temp[1]
            liste_moves.append(move)

        return liste_moves
