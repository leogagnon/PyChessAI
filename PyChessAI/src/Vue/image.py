import pygame
from abc import ABC, abstractmethod

class Image(ABC):
    def __init__(self, nom, position):
        """
        Toute forme d'image utilisée dans le programme
        :param nom: Nom de l'image
        :param position: Position (largeur,hauteur) en pixel
        """
        self.nom = nom
        self.position = position
        self.image = None
        self.dimension = None
        self.init_image()
        self.init_dimension()

    def init_image(self):
        """
        Initialise l'image
        Est overide dans toutes les classes filles
        """
        self.image = pygame.image.load("Vue\images\\" + self.nom + ".png")

    def init_dimension(self):
        """
        Initialise les dimentions de l'image
        """
        self.dimension = self.image.get_rect().size

    @staticmethod
    def DIMENSION_CASE():
        """
        :return: Valeur de la longeur d'un des côté d'une case
        """
        return 41

    @staticmethod
    def BOTTOM_LEFT():
        """
        :return: Valeur du coin en bas à droite de l'échiquier
        """
        return [24, 350]
















