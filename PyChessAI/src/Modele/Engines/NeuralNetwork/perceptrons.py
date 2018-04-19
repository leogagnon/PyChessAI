import random
import cmath


class Perceptrons:
    def __init__(self, size_input):
        '''
        Un perceptron est l'unité de calcul pour le NN (c'est le node dans la theorie des graphs pour les neurals network)
        :param size_input: c'est la quantité de input qui va venir (c'est pour savoir combien de weights sont nécessaire)
        '''
        self.weights = []
        self.initWeight(size_input)
        self.output = 0

    def initWeight(self, size_input):
        '''
        Donne des valeurs random au weights qui vont ensuite se faire changer pour modéliser la situation idéale
        :param size_input: la quantité de inputs pour savoir combien de weights on a besoin de créer
        '''

        for i in range(size_input):
            self.weights.append(random.random())

    #c'est une fonction qui est supposé remplacé un threshold discontinue (on veux que sa soit continue pour que sa puisse être différenciable)
    #si ce n'est pas différenciable on ne peut pas "backpropagate"
    @staticmethod
    def sigmoid(x):
        '''
        Calculer l'image d'une fonction à un point déterminé (le choix de la fonction est de même car il ressemble à une fonction par intervalle, mais c'est continu et facilement dérivable)
        :param x: le point qu'on a besoin de l'image
        :return: la valeur de l'image
        '''
        if x >= 100:
            return 1
        elif x <= -100:
            return 0
        return 1/(1 + cmath.pow(cmath.e, -x))
    @staticmethod
    def deriveSigmoid(x):
        '''
        La dérivé de la fonction sigmoid
        :param x: Le point qu'on a besoin de l'image de la dérivé de sigmoid
        :return: la valeur de l'image
        '''
        return Perceptrons.sigmoid(x) * (1 - Perceptrons.sigmoid(x))
