import pickle
from Modele.Elements.chevalier import Chevalier
from Modele.Elements.fou import Fou
from Modele.Elements.pion import Pion
from Modele.Elements.reine import Reine
from Modele.Elements.roi import Roi
from Modele.Elements.tour import Tour
from Modele.Engines.NeuralNetwork.network import Network
from Modele.Game.enums import TypePiece
from Modele.Game.game import Game


class TrainNeuralNetwork:
    def __init__(self, couleur):
        self.couleur = couleur
        self.RELATIVE_PATH = "../Engines/NeuralNetwork/"
        self.nn = Network(66)

    def train(self):
        depart = 0
        try:
            file = open(self.RELATIVE_PATH + "infoWeight.txt", "r")
            if bool(file.readline()):
                depart = int(file.readline())
                self.remplirWeight(self.RELATIVE_PATH + "weights")
        except Exception:
            file = open(self.RELATIVE_PATH + "infoWeight.txt", "w")
            file.write("False")
            file.close()

        for num in range(depart, 1718):

            with open( self.RELATIVE_PATH + "enter/data" + str(num) + ".pkl", "rb") as f:
                targetList = pickle.load(f)

            couleurBlanc = True
            self.initPiece()
            numero_move = 0
            for i in targetList:
                self.nn.learning(self.board, couleurBlanc, i[0:2], numero_move)
                self.mouvementMemory(i[0], i[1], i[2])
                couleurBlanc = not couleurBlanc
                numero_move += 1
            enter = []
            for i in self.nn.layers:
                temp = []
                for j in i:
                    temp.append(j.weights)
                enter.append(temp)

            with open(self.RELATIVE_PATH + "weights.pkl", "wb") as f:
                pickle.dump(enter, f)
            file = open(self.RELATIVE_PATH + "infoWeight.txt", "w")
            file.write("True\n")
            file.write(str(num + 1))
            file.close()

            print("done game")

    def mouvementMemory(self, lastPosition, position, promotedPiece):
        '''
        Sa va prendre une position de départ (lastPosition) et la position finale (position) et sa va modifier le board selon le move
        :param lastPosition: la position initiale de la pièce à bouger
        :param position: la position finale de la pièce à bouger
        '''
        if isinstance(self.board[lastPosition[0]][lastPosition[1]], Pion):
            if abs(position[0] - lastPosition[0]) == 1 and self.board[position[0]][position[1]] is None:
                self.board[position[0]][lastPosition[1]] = None

        self.board[position[0]][position[1]] = self.board[lastPosition[0]][lastPosition[1]]
        self.board[position[0]][position[1]].position = position
        self.board[lastPosition[0]][lastPosition[1]] = None

        if isinstance(self.board[position[0]][position[1]], Pion):
            if self.board[position[0]][position[1]].first:
                for temp in self.board:
                    for temp2 in temp:
                        if isinstance(temp2, Pion) and temp2.second:
                            temp2.second = False
                self.board[position[0]][position[1]].first = False
                if abs(lastPosition[1] - position[1]) == 2:
                    self.board[position[0]][position[1]].second = True
            elif self.board[position[0]][position[1]].second:
                self.board[position[0]][position[1]].second = False
        else:
            for temp in self.board:
                for temp2 in temp:
                    if isinstance(temp2, Pion) and temp2.second:
                        temp2.second = False

        if isinstance(self.board[position[0]][position[1]], Pion):
            if position[1] == 7 or position[1] == 0:
                self.__promotion(position, promotedPiece)
        elif isinstance(self.board[position[0]][position[1]], Tour):
            if not (self.board[position[0]][position[1]].moved):
                self.board[position[0]][position[1]].moved = True
        elif isinstance(self.board[position[0]][position[1]], Roi):
            if not self.board[position[0]][position[1]].moved:
                if lastPosition[0] - position[0] == -2:
                    self.mouvementMemory([7, position[1]], [position[0] - 1, position[1]], self.board)
                elif lastPosition[0] - position[0] == 2:
                    self.mouvementMemory([0, position[1]], [position[0] + 1, position[1]], self.board)
                self.board[position[0]][position[1]].moved = True

    def __promotion(self, position, promotedPiece):
        if promotedPiece == TypePiece.REINE:
            self.board[position[0]][position[1]] = Reine(position, self.couleur)
        elif promotedPiece == TypePiece.TOUR:
            self.board[position[0]][position[1]] = Tour(position, self.couleur)
        elif promotedPiece == TypePiece.FOU:
            self.board[position[0]][position[1]] = Fou(position, self.couleur)
        elif promotedPiece == TypePiece.CAVALIER:
            self.board[position[0]][position[1]] = Chevalier(position, self.couleur)

    def initPiece(self):
        '''
        Cela va tout simplement initialiser le board à son état normal (c-a-d que le board va se trouver comme si personne avait jouer un move)
        :return: sa ne return rien
        '''
        self.board = [[None for _ in range(8)] for _ in range(8)]
        for i in range(4):
            colum_reflechi = 7 - i
            if i == 0:
                self.board[i][0], self.board[colum_reflechi][0] = Tour([i, 0], True), Tour([colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Tour([i, 7], False), Tour([colum_reflechi, 7], False)
            elif i == 1:
                self.board[i][0], self.board[colum_reflechi][0] = Chevalier([i, 0], True), Chevalier(
                    [colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Chevalier([i, 7], False), Chevalier(
                    [colum_reflechi, 7], False)
            elif i == 2:
                self.board[i][0], self.board[colum_reflechi][0] = Fou([i, 0], True), Fou([colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Fou([i, 7], False), Fou([colum_reflechi, 7], False)
            elif i == 3:
                self.board[i][0], self.board[colum_reflechi][0] = Reine([i, 0], True), Roi([colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Reine([i, 7], False), Roi([colum_reflechi, 7], False)
        for i in range(8):
            self.board[i][1] = Pion([i, 1], True)
            self.board[i][6] = Pion([i, 6], False)

    def remplirWeight(self, path):
        temp = []
        with open(path + ".pkl", "rb") as f:
            temp = pickle.load(f)
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                self.nn.layers[i][j].weights = temp[i][j][:]

lol = TrainNeuralNetwork(True)
lol.train()