from Modele.AI.NeuralNetwork.perceptrons import Perceptrons
from Modele.Elements.pieceM import PieceM
from Modele.Game.enums import PieceChess
import Modele


class Network:

    def __init__(self, input_size):
        '''
        Créer le neural network (NN)
        :param input_size: va dire au NN la dimension du input qui s'en vient pour que la quantité de weights par perceptrons soit approprié
        '''
        nombre_layers = [50,40,32]
        input_sizes = [input_size] + nombre_layers[0:len(nombre_layers)-1]
        self.layers = [[Perceptrons(input_sizes[i]) for _ in range(nombre_layers[i])] for i in range(len(nombre_layers))]
        self.input = None
        self.index_targetList = 0

    def remplir(self):
        '''
        remplir les outputs de chacun des perceptrons
        :param input: va donner les inputs pour le premier layer du NN
        '''
        for i in range(len(self.layers[0])):
            self.layers[0][i].output = Perceptrons.sigmoid(sum(self.input[j]*self.layers[0][i].weights[j] for j in range(len(self.input))))
        if len(self.layers) > 1:
            for i in range(1, len(self.layers)): # from the first layer to the end
                for j in range(len(self.layers[i])): #for all the perceptrons in that layer
                    total = sum(self.layers[i-1][k].output * self.layers[i][j].weights[k] for k in range(len(self.layers[i-1])))
                    self.layers[i][j].output = Perceptrons.sigmoid(total)

    def totalInput(self, number_neuron, layer):
        '''
        prendre le total des inputs * les weights d'un perceptrons donnés
        :param number_neuron: savoir de quel perceptron on est entrain de parler
        :param layer: où se trouve le perceptron dans les layers
        :return: va return le total des inputs*les weights
        '''
        if layer == 0:
            return sum(self.layers[layer][number_neuron].weights[i] * self.input[i] for i in range(len(self.input)))
        return sum(self.layers[layer][number_neuron].weights[i] * self.layers[layer-1][i].output for i in range(len(self.layers[layer-1])))

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

    def createInput(self, board, couleur, numero_move):
        self.input = []
        for i in board:
            for j in i:
                multiplier = 1 if j is not None and j.couleurBlanc else -1
                if isinstance(j, Modele.Elements.pion.Pion):
                    self.input.append(multiplier*PieceChess.PION.value)
                elif isinstance(j, Modele.Elements.chevalier.Chevalier):
                    self.input.append(multiplier*PieceChess.CAVALIER.value)
                elif isinstance(j, Modele.Elements.fou.Fou):
                    self.input.append(multiplier*multiplier*PieceChess.FOU.value)
                elif isinstance(j, Modele.Elements.tour.Tour):
                    self.input.append(multiplier*PieceChess.TOUR.value)
                elif isinstance(j, Modele.Elements.reine.Reine):
                    self.input.append(multiplier*PieceChess.REINE.value)
                elif isinstance(j, Modele.Elements.roi.Roi):
                    self.input.append(multiplier*PieceChess.ROI.value)
                else:
                    self.input.append(PieceChess.NONE.value)
        color_value = 0 if couleur else 1
        self.input.append(color_value)
        self.input.append(numero_move)

    def calulate(self, board, couleur, numero_move):
        self.createInput(board, couleur, numero_move)
        self.remplir()
        allMoves = self.createAllMoves(board, couleur)
        indexBest, score = -1, -1

        for i in range(len(allMoves)):
            subtotal = 1
            for j in range(len(allMoves[i])):
                for k in range(len(allMoves[i][j])):
                    subtotal *= self.layers[len(self.layers)-1][allMoves[i][j][k] + (k+2*j)*8].output

            #print("move = " + str(allMoves[i]) + " ; subtotal = " + str(subtotal))
            if subtotal > score:
                indexBest, score = i, subtotal
        return allMoves[indexBest]


    def learning(self, board, couleur, targetList, numero_move):
        '''
        Cela est la partie où le programme essaye d'apprendre en ajustant tout simplement ces weights selon les fonctions dans les perceptrons et les targets (ce que des pros auraient joués)
        :param input: le input est le board dans un array et où les pièces sont remplacé par des valeurs numérique
        :return:
        '''
        self.createInput(board, couleur, numero_move)
        self.remplir()
        for i in range(len(self.layers)): # le numéro du layer
            for j in range(len(self.layers[i])): #parcours les percetrons du layer
                for k in range(len(self.layers[i][j].weights)): #parcours les weights du perceptron
                    self.layers[i][j].weights[k] -= self.recursive_function(i,j,targetList) * self.outputPerceptronBefore(i, k)

    def outputPerceptronBefore(self, layer, numero_perceptron):
        '''
        Va return le output du perceptron qui est pointé (si c'est le premeir layer le ouput est la valeur numérique à une postion dans le array qui représente le board)
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

        answer = Perceptrons.deriveSigmoid(self.totalInput(numero_perceptron, layer))
        if layer == len(self.layers)-1:
            value = targetList[int(numero_perceptron/16)][int(numero_perceptron/8) - 2*int(numero_perceptron/16)]
            target = 1 if value == numero_perceptron % 8 else 0
            return answer * (target - self.layers[layer][numero_perceptron].output)


        for i in range(len(self.layers[layer])):# tous les perceptrons dans le layer
            sub_total = self.recursive_function(layer+1, i, targetList)
            for j in range(len(self.layers[layer+1])): # parcourir
                answer += sub_total * self.layers[layer+1][j].weights[i]
            return answer