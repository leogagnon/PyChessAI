import pygame
from Vue.image import Image
#Ceci est la représention graphique d'une pièce
class Piece(Image):
    def __init__(self, nom, estBlanc, coordonnees):
        super().__init__(nom)
        self.estVert = False #True si la piece peux etre mangee
        self.estBlanc = estBlanc
        self.coordonnees = coordonnees
        self.bottom_left = [24, 350] # le bottom left de l'échiquier
        self.image = pygame.image.load("Vue\images\\" + nom + (" blanc" if self.estBlanc else " noir") + ".png")
        self.largeur, self.hauteur = self.image.get_rect().size
        self.position = [coordonnees[0] * self.dimension_case + self.bottom_left[0], -(self.coordonnees[1] + 1) * self.dimension_case + self.bottom_left[1]] #sa position dans l'interface

    #Changer la position (l'index dans lequel il va se trouver) et sa location (position dans l'interface)
    def setPosition(self, position):
        self.coordonnees = position
        self.location = [position[0] * self.dimension_case + self.bottom_left[0], -(self.coordonnees[1] + 1) * self.dimension_case + self.bottom_left[1]]


