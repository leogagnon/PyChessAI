from Modele.Engines.NeuralNetwork.perceptrons import Perceptrons
from Modele.Elements.pieceM import PieceM
from Modele.Game.enums import PieceChess
import Modele


class Network:

    def __init__(self, input_size):
        '''
        Créer le neural network (NN)
        :param input_size: va dire au NN la dimension du input qui s'en vient pour que la quantité de weights par perceptrons soit approprié
        '''
        nombre_layers = [15,10,32]
        input_sizes = [input_size] + nombre_layers[0:len(nombre_layers)-1]
        self.layers = [[Perceptrons(input_sizes[i]) for _ in range(nombre_layers[i])] for i in range(len(nombre_layers))]
        self.input = None

    def remplir(self):
        '''
        remplir les totals inputs et les outputs de tous les perceptrons
        :param input: va donner les inputs pour le premier layer du NN
        '''

        for i in range(len(self.layers)):
            for j in range(len(self.layers[i])):
                if i == 0 :
                    self.layers[i][j].totalInput = sum(self.input[k] * self.layers[i][j].weights[k] for k in range(len(self.input)))
                else:
                    self.layers[i][j].totalInput = sum(self.layers[i-1][k].output * self.layers[i][j].weights[k] for k in range(len(self.layers[i][j].weights)))
                self.layers[i][j].output = Perceptrons.sigmoid(self.layers[i][j].totalInput)

    def createAllMoves(self, board, couleur):
        '''
        Creer une liste de tous les mouvements possibles [départ, arrivé]
        :param board: une matrice de toutes les pièces
        :param couleur: c'est le tour de qui a jouer True -> blanc False -> noir
        :return: va return la liste des mouvements possibles
        '''
        allMoves = []
        for i in board:
            for j in i:
                if j is not None and j.couleurBlanc == couleur:
                    lastPosition = j.position
                    moves = board[lastPosition[0]][lastPosition[1]].possibiliteBouger(board)
                    posRoi = PieceM.trouverRoi(board, board[lastPosition[0]][lastPosition[1]].couleurBlanc)
                    board[posRoi[0]][posRoi[1]].acceptableMove(moves, board, lastPosition)
                    for temp1 in range(len(moves)):
                        for temp2 in range(len(moves[temp1])):
                            if moves[temp1][temp2]:
                                allMoves.append([lastPosition, [temp1, temp2]])
        return allMoves

    def createInput(self, board, couleur):
        self.input = []
        for i in board:
            for j in i:
                multiplier = 1/6 if j is not None and j.couleurBlanc else -1/6
                if isinstance(j, Modele.Elements.pion.Pion):
                    self.input.append(multiplier*PieceChess.PION.value)
                elif isinstance(j, Modele.Elements.chevalier.Chevalier):
                    self.input.append(multiplier*PieceChess.CAVALIER.value)
                elif isinstance(j, Modele.Elements.fou.Fou):
                    self.input.append(multiplier*PieceChess.FOU.value)
                elif isinstance(j, Modele.Elements.tour.Tour):
                    self.input.append(multiplier*PieceChess.TOUR.value)
                elif isinstance(j, Modele.Elements.reine.Reine):
                    self.input.append(multiplier*PieceChess.REINE.value)
                elif isinstance(j, Modele.Elements.roi.Roi):
                    self.input.append(multiplier*PieceChess.ROI.value)
                else:
                    self.input.append(PieceChess.NONE.value)
        color_value = -5 if couleur else 5
        self.input.append(color_value)

    def calculate(self, board, couleur):

        self.createInput(board, couleur)
        self.remplir()
        allMoves = self.createAllMoves(board, couleur)
        indexBest, score = -1, -1

        for i in range(len(allMoves)):
            subtotal = 1
            for j in range(len(allMoves[i])):
                for k in range(len(allMoves[i][j])):
                    subtotal *= self.layers[len(self.layers)-1][allMoves[i][j][k] + (k+2*j)*8].output
            if subtotal > score:
                indexBest, score = i, subtotal
        return allMoves[indexBest]


    def learning(self, board, couleur, targetList):
        '''
        Cela est la partie où le programme essaye d'apprendre en ajustant tout simplement ces weights selon les fonctions dans les perceptrons et les targets (ce que des pros auraient joués)
        :param input: le input est le board dans un array et où les pièces sont remplacé par des valeurs numérique
        :return:
        '''
        self.createInput(board, couleur)
        self.remplir()
        for l in range(len(self.layers)): # le numéro du layer
            for i in range(len(self.layers[l])): #parcours les percetrons du layer
                backpropagation = self.recursive_function(l, i, targetList)
                for j in range(len(self.layers[l][i].weights)): #parcours les weights du perceptron
                    before = self.outputPerceptronBefore(l, j)
                    if before != 0:
                        self.layers[l][i].weights[j] += backpropagation * before

    def outputPerceptronBefore(self, layer, numero_perceptron):
        '''
        Va return le output du perceptron qui est pointé (si c'est le premeir layer le output est la valeur numérique à une postion dans le array qui représente le board)
        :param layer: le layer où le perceptron se trouve
        :param numero_perceptron: l'index où se trouve le perceptron
        :return: Return le output
        '''
        if layer == 0:
            return self.input[numero_perceptron]
        return self.layers[layer-1][numero_perceptron].output

    def recursive_function(self, layer, numero_perceptron, targetList):
        '''
        La fonction récursive qui va "backpropagate" à travers le NN pour pouvoir correctement ajuster les weights des perceptrons
        :param layer: le numéro du layer
        :param numero_perceptron: l'index où se trouve le perceptron
        :param target: ce que le joueur professionnel aurait fait
        '''

        answer = Perceptrons.deriveSigmoid(self.layers[layer][numero_perceptron].totalInput)
        if layer == len(self.layers)-1:
            value = targetList[int(numero_perceptron/16)][int(numero_perceptron/8) - 2*int(numero_perceptron/16)]
            target = 1 if value == numero_perceptron%8 else 0
            return answer * (target - self.layers[layer][numero_perceptron].output)
        return answer * sum(self.recursive_function(layer+1, k, targetList) * self.layers[layer+1][k].weights[numero_perceptron] for k in range(len(self.layers[layer+1])))
