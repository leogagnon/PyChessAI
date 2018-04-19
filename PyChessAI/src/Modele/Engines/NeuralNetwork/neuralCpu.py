import pickle

from Modele.Engines.NeuralNetwork.network import Network
from Modele.Game.machine import Machine


class NeuralMachine(Machine):
    def __init__(self, couleur, game):
        super().__init__(couleur, game)
        self.board = self.game.board
        self.nn = Network(65)
        self.remplirWeight("Modele\Engines\\NeuralNetwork\weights")
        self.havePlayed = False

    def play(self):

        move = self.nn.calulate(self.board, self.COULEUR_BLANC)
        return move[0], move[1]

    def remplirWeight(self, path):
        try:
            temp = []
            with open(path + ".pkl", "rb") as f:
                temp = pickle.load(f)
            print(temp)
            for i in range(len(temp)):
                for j in range(len(temp[i])):
                    self.nn.layers[i][j].weights = temp[i][j][:]
        except Exception:
            print("commence sans les weights !!")


