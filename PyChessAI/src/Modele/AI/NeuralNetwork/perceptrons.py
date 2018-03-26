import random
import math

class Perceptrons:
    def __init__(self, size_input):
        self.weights = []
        self.initWeight(size_input)
        self.output = 0

    def initWeight(self, size_input):
        for i in range(size_input):
            self.weights.append(random.random())

    def fctOutput(self, input):
        self.output = sum(input[i]*self.weights[i] for i in range(len(input)))


    #c'est une fonction qui est supposé remplacé un threshold discontinue (on veux que sa soit continue pour que sa puisse être différenciable)
    #si ce n'est pas différenciable on ne peut pas "backpropagate"
    @staticmethod
    def sigmoid(y):
        return 1/(1+ math.e**-y)
    @staticmethod
    def deriveSigmoid(self, y):
        return Perceptrons.sigmoid(y) * (1 - Perceptrons.sigmoid(y))



