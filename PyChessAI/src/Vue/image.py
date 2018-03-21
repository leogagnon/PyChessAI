import pygame

class Image():
    def __init__(self, nom, position = None, initImage = False):

        """
        Toute forme d'image utilisée dans le programme
        :param nom: Nom de l'image
        :param position: Position (largeur,hauteur) en pixel
        :param initImage: Initialise l'image avec un fichier ayant comme nom : "nom".png
        """
        self.nom = nom
        self.position = position

        #Initialise l'image si indiqué dans l'appel
        if initImage:
            self.image = pygame.image.load("Vue\images\\" + nom + ".png ")
            self.largeur, self.hauteur = self.image.get_rect().size
        else:
            self.image = None
            self.largeur = None
            self.hauteur = None

        #Constantes en lien avec l'echiquier
        self.dimension_case = 41
        self.bottom_left = [24, 350]











