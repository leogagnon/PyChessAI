import pygame
from Vue.image import Image

class Bouton(Image):

    def __init__(self, nom, position):
        """

        :param nom: Nom
        :param position:
        """
        super().__init__(nom,position)
        self.image = pygame.image.load("Vue\\images\\button_" + nom + ".png")
        self.largeur, self.hauteur = self.image.get_rect().size
