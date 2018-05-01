import pickle

from Modele.Engines.NeuralNetwork.network import Network
from Modele.Game.machine import Machine


class NeuralMachine(Machine):
    def __init__(self, couleur, game):
        '''
        Sa va être la classe qui sera instancier lorsque le joueur aura indiquer qu'il veut un Neural Network
        :param couleur: la couleur de l'intelligence artificielle
        :param game: c'est la game qui est couramment en cours (pour lui donner de l'information sur son déroulement)
        '''
        super().__init__(couleur, game)
        self.board = self.game.board
        self.nn = Network(65)
        self.remplirWeight("Modele\Engines\\NeuralNetwork\weights")
        self.havePlayed = False

    def play(self):
        '''
        Va calculer quelle mouvement serait le plus optimal à commencer avec
        :return: le movement à faire move[0] -> la position initiale et move[1] -> la position finale
        '''
        move = self.nn.calculate(self.board, self.COULEUR_BLANC)

        return move[0], move[1]

    def remplirWeight(self, path):
        '''
        Va remplir les weights au NN grâce à des données qui ont été sauvée dans le projet
        :param path: où trouver les weights dans le projet
        '''
        try:
            temp = []
            with open(path + ".pkl", "rb") as f:
                temp = pickle.load(f)
            for i in range(len(temp)):
                for j in range(len(temp[i])):
                    self.nn.layers[i][j].weights = temp[i][j][:]
        except Exception:
            print("commence sans les weights !!")


