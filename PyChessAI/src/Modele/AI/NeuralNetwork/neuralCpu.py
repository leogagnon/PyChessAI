from Modele.Game.machine import Machine
from Modele.AI.NeuronNetwork.network import Network

class NeuralMachine(Machine):
    def __init__(self, couleur):
        super().__init__(couleur)
        self.nn = Network(5)

    def train(self):
        print("ouf im training")
    def play(self, board):
        print("hi")