from Modele.Players.cpu import Cpu
from Modele.AI.NeuralNetwork.network import Network

class NeuralCpu(Cpu):
    def __init__(self, couleur):
        super().__init__(couleur)
        self.nn = Network(5)

    def train(self):
        print("ouf im training")
    def play(self, board):
        print("hi")