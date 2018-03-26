import pygame
from Vue.image import Image

class Bouton(Image):

    def __init__(self, nom, position):
        super().__init__(nom,position)

    def init_image(self):
        self.image = pygame.image.load("Vue\\images\\button_" + self.nom + ".png")

