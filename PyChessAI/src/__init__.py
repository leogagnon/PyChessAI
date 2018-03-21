import pygame

from Modele.Elements.tour import Tour
from Modele.Elements.pieceM import PieceM
from Modele.Elements.roi import Roi
from Modele.Elements.reine import Reine
from Modele.Elements.chevalier import Chevalier
from Modele.Elements.fou import Fou
from Modele.Elements.pion import Pion
from Vue.piece import Piece
from Vue.vert import Vert
from Modele.Players.opponents import Opponents
from Modele.Elements.memoire import Memoire
from Vue.bouton import Bouton
from Vue.image import Image
from Modele.Players.enums import ModeDeJeu, TypePiece, MoveSpecial

class Chess():
    def __init__(self):

        """
        Constructeur : Initialisations des différents éléments nécéssaires au jeu
        """

        #Déclaration des différents images
        self.echiquierImage = Image('echiquier', [0, 0],True)
        self.modeDeJeu_buttons = [Bouton('homme-vs-homme', [0, 30 + 70 * 1]),
                                  Bouton('homme-vs-machine', [0, 30 + 70 * 2]),
                                  Bouton('machine-vs-machine', [0, 30 + 70 * 3])]

        self.undo_button = Bouton('undo', [self.echiquierImage.largeur + 25, 125 + 40 * 5])
        self.list_button = Bouton('list-moves', [self.echiquierImage.largeur + 25, 125 + 40 * 4])

        #Déclaration des tableaux
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.listePiece = [[None for _ in range(8)] for _ in range(8)]
        self.listeVert = []
        self.positionCurseur = []
        self.lastPosition = [0,0]

        #Indique qui commence la partie
        Opponents.tourBlanc = True

        #Indique le mode de jeu choisi (par défaut JOUEUR_JOUEUR)
        self.modeDeJeu = ModeDeJeu.JOUEUR_JOUEUR

        #Initialisation de la fenetre de PyGame
        self.init_pygame()

    def main_loop(self):

        """
        Fonctionnement logique de la partie
        """

        self.init_main()

        #Indique si la partie est terminée
        done = False
        #Valeurs temporaires utilisées pour faire des évaluations

        vert = None

        #Boucle principale
        while not done:
            if Opponents.playerTourHumain():
                #Passe à travers tout les events détectés par PyGame
                for event in pygame.event.get():
                    pieceTemp = None
                    if event.type == pygame.QUIT:
                        done = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.positionCurseur = pygame.mouse.get_pos()
                        for i in self.listePiece:
                            for j in i:
                                if j != None and j.image.get_rect().move(j.position[0], j.position[1]).collidepoint(self.positionCurseur):
                                    pieceTemp = j
                        if pieceTemp != None and (Opponents.tourBlanc == pieceTemp.estBlanc or pieceTemp.estVert):
                            self.clicked(pieceTemp)
                        vert = None
                        for temp in self.listeVert:
                            if temp.image.get_rect().move(temp.position[0], temp.position[1]).collidepoint(self.positionCurseur):
                                vert = temp

                        if vert != None:
                            self.clickedVert(vert)
                            #si on clique sur le boutton undo (commentaire pour le if suivant)
                        elif Memoire.numero_move != 0 and self.undo_button.image.get_rect().move(self.undo_button.position[0], self.undo_button.position[1]).collidepoint(self.positionCurseur):
                            Memoire.undo(self.board)
                            self.boardToInterface()
                            # si on clique sur le boutton liste_move (commentaire pour le if suivant) -> va afficher tous les moves réalisé
                        #elif self.list_button.image.get_rect().move(self.list_button.largeur, self.list_button.hauteur).collidepoint(positionCurseur):
                            #master = Tk()
                            #lb = Listbox(master)
                            #for i in range(len(Memoire.tous_move)):
                            #    lb.insert(i, Memoire.tous_move[i])
                            #lb.pack()
                            #master.mainloop()


            else:
                special = Opponents.getPlayerTour().play(self.board)
                self.boardToInterface()

            pygame.display.flip()
        pygame.display.quit()

    def init_pygame(self):
        """
        Initialise l'interface PyGame
        """
        self.screen = pygame.display.set_mode((self.echiquierImage.largeur + 200, self.echiquierImage.hauteur))
        pygame.init()
        pygame.display.set_caption("Chess program")

    def init_main(self):
        """
        Initialise la partie
        """
        Opponents(self.modeDeJeu.value, self.screen)

        self.screen.blit(self.echiquierImage.image, self.echiquierImage.position)
        self.init_pieces()

        self.screen.blit(self.undo_button.image, self.undo_button.position)
        self.screen.blit(self.list_button.image, self.list_button.position)

        pygame.display.flip()

    def init_intro(self):

        """
        Initialise l'écran d'intro
        """
        self.screen.blit(self.modeDeJeu_buttons[0].image, self.modeDeJeu_buttons[0].position)
        self.screen.blit(self.modeDeJeu_buttons[1].image, self.modeDeJeu_buttons[1].position)
        self.screen.blit(self.modeDeJeu_buttons[2].image, self.modeDeJeu_buttons[2].position)
        pygame.display.flip()



    def intro_loop(self):

        """
        Fonctionnement logique de l'intro
        """

        #Indique lorsqu'il faut quitter l'intro
        done = False

        self.init_intro()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    positionCurseur = pygame.mouse.get_pos()



        #Réinitialise l'écran en le remplissant avec du noir
        self.screen.fill((0,0,0))

    def clickedVert(self,vert):
        """
        Déplace la pièce séclectionnée sur la case verte sélectionnée
        :param vert: Objet Vert sur lequel le joueur clique
        """
        coordonnees = vert.coordonnees[:]
        special = self.board[self.lastPosition[0]][self.lastPosition[1]].mouvementMemory(coordonnees, self.lastPosition, self.board)
        self.mouvementInterface(coordonnees, self.lastPosition, special)
        Memoire.move_made(coordonnees, self.lastPosition, self.board[coordonnees[0]][coordonnees[1]], None, special)

    def clicked(self, piece):
        """
        Offre les coups possibles au joueur lorsqu'il sélectionne une pièce
        :param piece: Pièce sélectionnée
        """
        coordonnees = piece.coordonnees[:]
        if piece.estVert:
            pieceTemp = self.board[coordonnees[0]][coordonnees[1]]
            special = self.board[self.lastPosition[0]][self.lastPosition[1]].mouvementMemory(coordonnees, self.lastPosition, self.board)
            self.mouvementInterface(coordonnees, self.lastPosition, special)
            Memoire.move_made(coordonnees, self.lastPosition, self.board[coordonnees[0]][coordonnees[1]], pieceTemp, special)
        else:
            self.nouveau()
            moves = self.board[coordonnees[0]][coordonnees[1]].possibiliteBouger(self.board)
            posRoi = PieceM.trouverRoi(self.board, self.board[coordonnees[0]][coordonnees[1]].couleurBlanc)
            self.board[posRoi[0]][posRoi[1]].acceptableMove(moves, self.board, coordonnees)

            for i in range(len(moves)):
                for j in range(len(moves[i])):
                    if moves[i][j]:
                        if self.listePiece[i][j] == None:
                            self.listeVert.append(Vert([i,j]))
                        else:
                            self.listePiece[i][j].estVert = True
                            vertTemp = Vert([i,j])
                            self.screen.blit(vertTemp.image, vertTemp.position)
                            self.screen.blit(self.listePiece[i][j].image, self.listePiece[i][j].position)

            for vert in self.listeVert:
                self.screen.blit(vert.image, vert.position)
                self.lastPosition = coordonnees[:]



    def boardToInterface(self):
        """
        Met à jour l'affichage en fonction de l'état de self.board
        """
        self.listePiece = [[None for i in range(8)] for j in range(8)]

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is not None:
                    if isinstance(self.board[i][j], Roi):
                        self.listePiece[i][j] = Piece("roi", self.board[i][j].couleurBlanc, self.board[i][j].position)
                    elif isinstance(self.board[i][j], Reine):
                        self.listePiece[i][j] = Piece("reine", self.board[i][j].couleurBlanc, self.board[i][j].position)
                    elif isinstance(self.board[i][j], Tour):
                        self.listePiece[i][j] = Piece("tour", self.board[i][j].couleurBlanc,self.board[i][j].position)
                    elif isinstance(self.board[i][j], Fou):
                        self.listePiece[i][j] = Piece("fou", self.board[i][j].couleurBlanc, self.board[i][j].position)
                    elif isinstance(self.board[i][j], Chevalier):
                        self.listePiece[i][j] = Piece("cavalier", self.board[i][j].couleurBlanc, self.board[i][j].position)
                    elif isinstance(self.board[i][j], Pion):
                        self.listePiece[i][j] = Piece("pion", self.board[i][j].couleurBlanc, self.board[i][j].position)
        self.nouveau()

    def nouveau(self):
        """
        Met à jour l'apparence du jeu (déselectionne tout ce qui est sélectionné)
        """
        self.screen.fill((0,0,0))
        self.screen.blit(self.echiquierImage.image, (0,0))
        self.screen.blit(self.undo_button.image, self.undo_button.position)
        self.screen.blit(self.list_button.image, self.list_button.position)

        for i in self.listePiece:
            for j in i:
                if j is not None:
                    if j.estVert:
                        j.estVert = False
                    self.screen.blit(j.image, j.position)
        self.listeVert.clear()

    def init_pieces(self):
        """
        Initialise la self.board avec les pièces au début de chaque partie
        """
        for i in range(4):
            colum_reflechi = 7 - i
            if i == 0:
                self.board[i][0], self.board[colum_reflechi][0]  = Tour([i,0], True), Tour([colum_reflechi,0], True)
                self.board[i][7], self.board[colum_reflechi][7]  = Tour([i, 7], False), Tour([colum_reflechi, 7], False)
            elif i==1:
                self.board[i][0], self.board[colum_reflechi][0] = Chevalier([i,0], True), Chevalier([colum_reflechi,0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Chevalier([i, 7], False), Chevalier([colum_reflechi, 7], False)
            elif i == 2:
                self.board[i][0], self.board[colum_reflechi][0] = Fou([i,0], True), Fou([colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Fou([i,7], False), Fou([colum_reflechi, 7], False)
            elif i == 3:
                self.board[i][0], self.board[colum_reflechi][0] = Reine([i,0], True), Roi([colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Reine([i, 7], False), Roi([colum_reflechi, 7], False)
        for i in range(8):
            self.board[i][1] = Pion([i,1], True)
            self.board[i][6] = Pion([i,6], False)

        ordre = [TypePiece.TOUR,
                 TypePiece.CAVALIER,
                 TypePiece.FOU,
                 TypePiece.REINE,
                 TypePiece.ROI,
                 TypePiece.FOU,
                 TypePiece.CAVALIER,
                 TypePiece.TOUR]
        for i in range(8):
            self.listePiece[i][0] = Piece(ordre[i].name, True, [i,0])
            self.listePiece[i][1] = Piece("pion", True, [i,1])
            self.listePiece[i][7] = Piece(ordre[i].name, False, [i, 7])
            self.listePiece[i][6] = Piece("pion", False, [i, 6])
        for i in self.listePiece:
            for j in i:
                if j is not None:
                    self.screen.blit(j.image, j.position)

    def mouvementInterface(self, position, lastPosition, move_special):

        """
        Déplace visuellement la pièce sélectionnée (prends en compte les mouvements spéciaux)
        :param position:
        :param lastPosition:
        :param move_special:
        """
        self.listePiece[position[0]][position[1]] = self.listePiece[lastPosition[0]][lastPosition[1]]
        self.listePiece[lastPosition[0]][lastPosition[1]].setPosition(position)
        self.listePiece[lastPosition[0]][lastPosition[1]] = None

        if move_special == MoveSpecial.PRISE_EN_PASSANT:
            self.listePiece[position[0]][lastPosition[1]] = None
        elif move_special == MoveSpecial.PROMOTION:
            inputs = ""

            if isinstance(self.board[position[0]][position[1]], Reine):
                inputs = Pion.getChoices()[0]
            elif isinstance(self.board[position[0]][position[1]], Tour):
                inputs = Pion.getChoices()[1]
            elif isinstance(self.board[position[0]][position[1]], Fou):
                inputs = Pion.getChoices()[2]
            elif isinstance(self.board[position[0]][position[1]], Chevalier):
                inputs = Pion.getChoices()[3]
            tempPiece = Piece(inputs, self.listePiece[position[0]][position[1]].couleur, position)
            self.listePiece[position[0]][position[1]] = tempPiece
        elif move_special == MoveSpecial.ROQUE:
            if lastPosition[0] - position[0] == -2:
                self.listePiece[position[0] - 1][position[1]] = self.listePiece[7][position[1]]
                self.listePiece[position[0] - 1][position[1]].setPosition([position[0]-1, position[1]])
                self.listePiece[7][position[1]] = None
            elif lastPosition[0] - position[0] == 2:
                self.listePiece[position[0] + 1][position[1]] = self.listePiece[0][position[1]]
                self.listePiece[position[0] + 1][position[1]].setPosition([position[0] + 1, position[1]])
                self.listePiece[0][position[1]] = None

        self.boardToInterface()


chess_init = Chess()
#chess_init.intro_loop()
chess_init.main_loop()
