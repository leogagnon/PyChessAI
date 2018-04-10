from abc import ABC

from Modele.Engines.ucip import UCIP
from Modele.Game.enums import *
from Modele.Game.machine import Machine
from Modele.Game.memoire import Memoire


class UCIP_Engine(Machine, ABC):
    """Classe abstraite représentant tous les engines utilisant le Universal Chess Interface Protocol (UCIP)"""

    def __init__(self, couleur, depth, game, command):
        self.engine = UCIP(command=command, depth=depth)
        self.promotion = None
        super().__init__(couleur, game)

    def play(self):
        """
        Voir classe mère
        :return: Le meilleur move
        """
        self.engine.set_position(self.get_liste_moves(self.game.memoire.tous_move))
        best_move = self.engine.get_best_move()
        best_move = self.check_promotion(best_move)
        self.lastPosition = Memoire.cipher(best_move[:2])
        self.position = Memoire.cipher(best_move[-2:])

        return (self.lastPosition, self.position)

    def get_liste_moves(self, tous_moves):
        """
        Transforme la liste de coup de générée par la mémoire en tableau de String -> ex. ['e2e4', 'e7e6']
        :return: La liste de coups
        """
        liste_moves = []

        for i in tous_moves:

            split = i.split(':')
            temp = i.split(':')[1].split('-')
            move = temp[0] + temp[1]

            # Si le move indique une promotion (P:e7-e8:Q), l'indique dans le string (ex. e7e8q)
            if len(split) == 3:
                move += split[2].lower()

            liste_moves.append(move)

        return liste_moves

    def check_promotion(self, move):
        """
        Vérifie si le move implique une promotion.
        Si oui : change self.promotion à la pièce choisie
        Si non : ne fait rien
        :param move: Move donné par l'engine (ex. e6e7 ou e7e8q pour promotion)
        :return: Le move donné en paramètre (moin la promotion si il y en avait une)
        """
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
