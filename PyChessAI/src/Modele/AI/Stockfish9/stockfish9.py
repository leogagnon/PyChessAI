from stockfish import Stockfish
from Modele.Players.machine import Machine
from Modele.Elements.memoire import Memoire
import Modele


class Stockfish9(Machine):
    def __init__(self, couleur, depth):
        self.stockfish = Stockfish(path='Modele/AI/Stockfish9/stockfish',depth=depth)
        super().__init__(couleur, depth)

    def play(self, board):
        self.stockfish.set_position(self.get_liste_moves())
        best_move = self.stockfish.get_best_move()


        self.lastPosition = Memoire.cipher(best_move[:2])
        self.position = Memoire.cipher(best_move[-2:])

        pieceTemp = board[self.position[0]][self.position[1]]
        special = board[self.lastPosition[0]][self.lastPosition[1]].mouvementMemory(self.position, self.lastPosition,board)
        Modele.Elements.memoire.Memoire.move_made(self.position, self.lastPosition, board[self.position[0]][self.position[1]], pieceTemp, special)

    def get_liste_moves(self):
        liste_moves = []

        for i in Memoire.tous_move:
            temp = i.split(':')[1].split('-')
            move = temp[0] + temp[1]
            liste_moves.append(move)

        return liste_moves
