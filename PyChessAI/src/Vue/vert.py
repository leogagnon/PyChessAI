import pygame
from Vue.image import Image

class Vert(Image):

    def __init__(self, coordonnees):
        self.coordonnees = coordonnees
        super().__init__('vert', [coordonnees[0] * Image.DIMENSION_CASE() + Image.BOTTOM_LEFT()[0], -(self.coordonnees[1] + 1) * Image.DIMENSION_CASE() + Image.BOTTOM_LEFT()[1]])


    def init_image(self):
        self.image = pygame.image.load("Vue\images\\" + self.nom + ".png")


