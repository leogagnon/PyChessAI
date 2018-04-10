from Modele.Game.machine import Machine
from Modele.AI.NeuralNetwork.network import Network
from Modele.Elements.pion import Pion
from Modele.Elements.chevalier import Chevalier
from Modele.Elements.fou import Fou
from Modele.Elements.tour import Tour
from Modele.Elements.reine import Reine
from Modele.Elements.roi import Roi
import pickle
import Modele

class NeuralMachine(Machine):
    def __init__(self, couleur):
        super().__init__(couleur)
        self.nn = Network(66)
        self.havePlayed = False

    def train(self):
        depart = 0
        try:
            file = open("infoWeight.txt", "r")
            if bool(file.readline()):
                depart = int(file.readline())
                self.remplirWeight("weights")
        except Exception:
            file = open("infoWeight.txt", "w")
            file.write("False")
            file.close()

        for num in range(depart, 1718):
            targetList = self.remplirTargetList(num)
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
            
            with open("weights.pkl", "wb") as f:
                pickle.dump(enter, f)
            file = open("infoWeight.txt", "w")
            file.write("True\n")
            file.write(str(num+1))
            file.close()

            print("done game")

    def mouvementMemory(self, lastPosition, position, promotedPiece):
        '''
        Sa va prendre une position de départ (lastPosition) et la position finale (position) et sa va modifier le board selon le move
        :param lastPosition: la position initiale de la pièce à bouger
        :param position: la position finale de la pièce à bouger
        '''
        if isinstance(self.board[lastPosition[0]][lastPosition[1]], Pion):
            self.board[lastPosition[0]][lastPosition[1]].ongoingPassant(position, lastPosition, self.board)

        self.board[position[0]][position[1]] = self.board[lastPosition[0]][lastPosition[1]]
        self.board[position[0]][position[1]].position = position
        self.board[lastPosition[0]][lastPosition[1]] = None

        self.board[position[0]][position[1]].prisePassant(lastPosition, self.board)

        if isinstance(self.board[position[0]][position[1]], Pion):
            if position[1] == 7 or position[1] == 0:
                self.board[position[0]][position[1]].promotion(promotedPiece, self.board)
        elif isinstance(self.board[position[0]][position[1]], Tour):
            if not (self.board[position[0]][position[1]].moved):
                self.board[position[0]][position[1]].moved = True
        elif isinstance(self.board[position[0]][position[1]], Roi):
            if not self.board[position[0]][position[1]].moved:
                if lastPosition[0] - position[0] == -2:
                    self.board[7][position[1]].mouvementMemory([position[0] - 1, position[1]], [7, position[1]], self.board)
                elif lastPosition[0] - position[0] == 2:
                    self.board[0][position[1]].mouvementMemory([position[0] + 1, position[1]], [0, position[1]], self.board)
                self.board[position[0]][position[1]].moved = True

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

    def remplirTargetList(self, index):
        '''
        Sa remplit une liste de ce qu'une personne professionnelle à jouer lors d'une game
        :param index: c'est le numéro de la game
        '''
        targetList = None
        with open("enter/data" + str(index) + ".pkl", "rb") as f:
            targetList = pickle.load(f)
        return targetList

    def play(self, board):
        self.position = None
        self.lastPosition = None
        self.remplirWeight("Modele\AI\\NeuralNetwork\weights")
        move = self.nn.calulate(board, self.COULEUR_BLANC, Modele.Elements.memoire.Memoire.numero_move)
        self.lastPosition , self.position = move[0], move[1]

        pieceTemp = board[self.position[0]][self.position[1]]
        special = board[self.lastPosition[0]][self.lastPosition[1]].mouvementMemory(self.position, self.lastPosition, board)
        Modele.Elements.memoire.Memoire.move_made(self.position, self.lastPosition, board[self.position[0]][self.position[1]], pieceTemp, special)
        return special

    def remplirWeight(self, path):
        temp = []
        with open(path + ".pkl", "rb") as f:
            temp = pickle.load(f)
        print(temp)
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                self.nn.layers[i][j].weights = temp[i][j][:]


#lol = NeuralMachine(True)
#lol.train()