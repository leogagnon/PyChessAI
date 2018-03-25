from Modele.Players.joueur import Joueur
import pygame
from Vue.bouton import Bouton
from Modele.Elements.pion import Pion
import Modele

#Cela est l'équivalent du joueur humain qui va pouvoir jouer (cela ne sera utile que pour la classe Opponents)
class Humain(Joueur):
    #le constructeur
    def __init__(self, couleurBlanc):
        super().__init__(couleurBlanc)
        self.echiquierImageCote = 373

    #demander à l'utilisateur qu'elle pièce prendre la place du pion qui est en train d'avoir une promotion
    def choixPromotion(self, board, position):
        input_number = -1
        listeButton = []
        pygame.font.init()
        myfont = pygame.font.SysFont("Comic Sans MS", 25)
        text_surface = myfont.render("Promotion : ", False, (255, 255, 255))
        Modele.Players.opponents.Opponents.screen.blit(text_surface, (self.echiquierImageCote + 10, 30))

        for i in range(4):
            listeButton.append(Bouton(Pion.getChoices()[i].name, [self.echiquierImageCote + 10, 100 + 40 * i]))
            Modele.Players.opponents.Opponents.screen.blit(listeButton[i].image, listeButton[i].position)

        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    positionCurseur = pygame.mouse.get_pos()
                    for i in range(len(listeButton)):
                        if listeButton[i].image.get_rect().move(listeButton[i].position).collidepoint(positionCurseur):
                            input_number = i
                            done = True
            pygame.display.flip()
        return Pion.getChoices()[input_number]

