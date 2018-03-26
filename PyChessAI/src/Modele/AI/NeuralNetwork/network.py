from Modele.AI.NeuronNetwork.perceptrons import Perceptrons


class Network:
    def __init__(self, input_size):
        nombre_layers = [7,4,2]
        input_sizes = [input_size] + nombre_layers[0:len(nombre_layers)-1]
        self.layers = [[Perceptrons(input_sizes[i]) for _ in range(nombre_layers[i])] for i in range(len(nombre_layers))]
        self.input = None

    def remplir(self, input):
        self.input = input[:]
        for i in range(len(self.layers[0])):
            self.layers[0][i].fctOutput(input)
        if len(self.layers) > 1:
            for i in range(1, len(self.layers)):
                for j in range(len(self.layers[i])):
                    total = sum(self.layers[i-1][k].output * self.layers[i][j].weights[k] for k in range(self.layers[i-1][k]))
                    self.layers[i][j].fctOutput(total)


    def documentInterpreter(self, board, move, couleur):
        position = None


        if move == "O-O":
            position = []
        elif len(move) == 2:
            position = []



    def totalInput(self, number_neuron, layer):
        if layer == 0:
            return sum(self.layers[layer][number_neuron].weights[i] * self.input[i] for i in range(len(self.input)))
        return sum(self.layers[layer][number_neuron].weights[i] * self.layers[layer-1][i].output for i in range(len(self.layers[layer-1])))

    #def findTarget(self):


    def learning(self, input):
        self.remplir(input)

        target = 0#self.findTarget()

        for i in range(len(self.layers)): # le numéro du layer
            for j in range(len(self.layers[i])): #parcours les percetrons du layer
                for k in range(len(self.layers[i][j].weights)): #parcours les weights du perceptron
                    self.layers[i][j].weights[j] += - self.recursive_function(i,j,target) * self.otherPartFunction(i, k)



    def otherPartFunction(self, layer, numero_perceptron):
        if layer == 0:
            return self.input[numero_perceptron]
        return self.layers[layer-1][numero_perceptron].output


    def recursive_function(self, layer, numero_perceptron, target):
        if layer == len(self.layers):
            return self.layers[layer][numero_perceptron].deriveSigmoid(self.totalInput(numero_perceptron, layer)) * (target - self.layers[layer][numero_perceptron].output)

        answer = self.layers[layer][numero_perceptron].deriveSigmoid(self.totalInput(numero_perceptron, layer))
        for i in range(len(self.layers[layer+1])):
            sub_total = self.recursive_function(layer+1, i)
            for j in range(len(self.layers[layer+1][i].weights)):
                answer += sub_total * self.layers[layer+1][i].weights[j]

