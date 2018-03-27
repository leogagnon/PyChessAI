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
import Modele
from Modele.Players.machine import Machine
from Modele.Players.machine import TypeAI
from Modele.Players.game import Game
from Modele.Elements.memoire import Memoire
from Vue.bouton import Bouton
from Vue.image import Image
from Modele.Players.humain import Humain
from Modele.Players.enums import ModeDeJeu, TypePiece, MoveSpecial
import easygui
import sys


class Chess():
    def __init__(self):

        """
        Constructeur : Initialisations des différents éléments nécéssaires au jeu
        """
        # Déclaration des différents images
        self.echiquier = Image('echiquier', [0, 0])
        self.undo_button = Bouton('undo', [self.echiquier.dimension[0] + 25, 125 + 40 * 5])
        self.list_button = Bouton('list-moves', [self.echiquier.dimension[1] + 25, 125 + 40 * 4])

        # Déclaration des tableaux
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.liste_piece = [[None for _ in range(8)] for _ in range(8)]
        self.liste_vert = []
        self.position_curseur = []
        self.lastPosition = [0, 0]

        # Indique le mode de jeu choisi (par défaut JOUEUR_JOUEUR)
        self.mode_de_jeu = ModeDeJeu.JOUEUR_JOUEUR

        # Initialisation de la fenetre de PyGame
        self.init_pygame()

    def main(self):
        pass

    def game_loop(self):
        """
        Fonctionnement logique de la partie
        """
        Game(self.mode_de_jeu, True, TypeAI.ALPHA_BETA,TypeAI.ALPHA_BETA)

        self.echiquier.blit(self.screen)
        self.init_pieces()
        self.undo_button.blit(self.screen)
        self.list_button.blit(self.screen)

        pygame.display.flip()

        #Indique si la partie est terminée
        done = False

        #Boucle principale
        while not done:
            if isinstance(Game.get_tour(), Humain):
                for event in pygame.event.get():
                    pieceTemp = None
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.position_curseur = pygame.mouse.get_pos()
                        for i in self.liste_piece:
                            for j in i:
                                if j is not None and j.image.get_rect().move(j.position[0], j.position[1]).collidepoint(
                                        self.position_curseur):
                                    pieceTemp = j

                        if pieceTemp is not None and (Game.tour_blanc == pieceTemp.estBlanc or pieceTemp.estVert):
                            self.clicked(pieceTemp)
                        vert = None
                        for temp in self.liste_vert:
                            if temp.image.get_rect().move(temp.position[0], temp.position[1]).collidepoint(
                                    self.position_curseur):
                                vert = temp

                        if vert is not None:
                            self.clickedVert(vert)
                            # si on clique sur le boutton undo (commentaire pour le if suivant)
                        elif Memoire.numero_move != 0 and self.undo_button.image.get_rect().move(
                                self.undo_button.position[0], self.undo_button.position[1]).collidepoint(
                            self.position_curseur):
                            if self.mode_de_jeu == ModeDeJeu.JOUEUR_JOUEUR:
                                Memoire.undo(self.board)
                            else:
                                Memoire.undo(self.board)
                                Memoire.undo(self.board)
                            self.boardToInterface()
                        elif self.list_button.image.get_rect().move(self.list_button.position[0],
                                                                    self.list_button.position[1]).collidepoint(
                            self.position_curseur):
                            easygui.textbox('Liste des moves', 'Liste', Memoire.tous_move)

                        posRoi = PieceM.trouverRoi(self.board, Game.tour_blanc)
                        if self.board[posRoi[0]][posRoi[1]].mat(self.board):
                            done = True



            else:
                # pour voir s'il est en mat en premier ou sinon erreur
                posRoi = PieceM.trouverRoi(self.board, Game.tour_blanc)
                if self.board[posRoi[0]][posRoi[1]].mat(self.board):
                    done = True

                Game.get_tour().play(self.board)
                self.boardToInterface()

                # voir si le joueur est mat ou sinon il peut pas jouer
                posRoi = PieceM.trouverRoi(self.board, Game.tour_blanc)
                if self.board[posRoi[0]][posRoi[1]].mat(self.board):
                    done = True

            pygame.display.flip()

    def init_pygame(self):
        """
        Initialise l'interface PyGame
        """
        self.screen = pygame.display.set_mode((self.echiquier.dimension[0] + 200, self.echiquier.dimension[1]))
        pygame.init()
        pygame.display.set_caption("Chess program")

    def outro_loop(self):
        """
        Fonctionnement logique de la conclusion
        """

    def init_timer(self, pos):
        pass

    def intro_loop(self):
        """
        Fonctionnement logique de l'introduction
        """
        choix = None

        HH_button = Bouton('homme-vs-homme', [(self.echiquier.dimension[0] - 50) / 2, 30 + 70 * 2])
        HM_button = Bouton('homme-vs-machine', [(self.echiquier.dimension[0] - 50) / 2, 30 + 70 * 3])
        MM_button = Bouton('machine-vs-machine', [(self.echiquier.dimension[0] - 50) / 2, 30 + 70 * 4])

        police = pygame.font.SysFont('arial', 50)
        message = police.render('Modes de jeu', 1, (255, 255, 255))

        image_gauche = Image('roi blanc', (0, 10))

        self.screen.blit(message, (self.echiquier.dimension[0] / 2 - 25, 50))
        HH_button.blit(self.screen)
        HM_button.blit(self.screen)
        MM_button.blit(self.screen)

        pygame.display.flip()

        #Boucle principale
        while choix is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.position_curseur = pygame.mouse.get_pos()

                    if HH_button.image.get_rect().move(HH_button.position[0], HH_button.position[1]).collidepoint(
                            self.position_curseur):
                        choix = ModeDeJeu.JOUEUR_JOUEUR
                    elif HM_button.image.get_rect().move(HM_button.position[0], HM_button.position[1]).collidepoint(
                            self.position_curseur):
                        choix = ModeDeJeu.JOUEUR_MACHINE
                    elif MM_button.image.get_rect().move(MM_button.position[0], MM_button.position[1]).collidepoint(
                            self.position_curseur):
                        choix = ModeDeJeu.MACHINE_MACHINE

        #Réinitialise l'écran en le remplissant avec du noir
        self.screen.fill((0, 0, 0))
        self.mode_de_jeu = choix

    def clickedVert(self, vert):
        """
        Déplace la pièce séclectionnée sur la case verte sélectionnée
        :param vert: Objet Vert sur lequel le joueur clique
        """
        coordonnees = vert.coordonnees[:]
        special = self.board[self.lastPosition[0]][self.lastPosition[1]].mouvementMemory(coordonnees, self.lastPosition,
                                                                                         self.board)
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
            special = self.board[self.lastPosition[0]][self.lastPosition[1]].mouvementMemory(coordonnees,
                                                                                             self.lastPosition,
                                                                                             self.board)
            self.mouvementInterface(coordonnees, self.lastPosition, special)
            Memoire.move_made(coordonnees, self.lastPosition, self.board[coordonnees[0]][coordonnees[1]], pieceTemp,
                              special)
        else:
            self.nouveau()
            moves = self.board[coordonnees[0]][coordonnees[1]].possibiliteBouger(self.board)
            posRoi = PieceM.trouverRoi(self.board, self.board[coordonnees[0]][coordonnees[1]].couleurBlanc)
            self.board[posRoi[0]][posRoi[1]].acceptableMove(moves, self.board, coordonnees)

            for i in range(len(moves)):
                for j in range(len(moves[i])):
                    if moves[i][j]:
                        if self.liste_piece[i][j] == None:
                            self.liste_vert.append(Vert([i, j]))
                        else:
                            self.liste_piece[i][j].estVert = True
                            vertTemp = Vert([i, j])
                            vertTemp.blit(self.screen)
                            self.liste_piece[i][j].blit(self.screen)

            for vert in self.liste_vert:
                vert.blit(self.screen)
            self.lastPosition = coordonnees[:]

    def boardToInterface(self):
        """
        Met à jour l'affichage en fonction de l'état de self.board
        """
        self.liste_piece = [[None for i in range(8)] for j in range(8)]

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is not None:
                    if isinstance(self.board[i][j], Roi):
                        self.liste_piece[i][j] = Piece("roi", self.board[i][j].couleurBlanc, self.board[i][j].position)
                    elif isinstance(self.board[i][j], Reine):
                        self.liste_piece[i][j] = Piece("reine", self.board[i][j].couleurBlanc,
                                                       self.board[i][j].position)
                    elif isinstance(self.board[i][j], Tour):
                        self.liste_piece[i][j] = Piece("tour", self.board[i][j].couleurBlanc, self.board[i][j].position)
                    elif isinstance(self.board[i][j], Fou):
                        self.liste_piece[i][j] = Piece("fou", self.board[i][j].couleurBlanc, self.board[i][j].position)
                    elif isinstance(self.board[i][j], Chevalier):
                        self.liste_piece[i][j] = Piece("cavalier", self.board[i][j].couleurBlanc,
                                                       self.board[i][j].position)
                    elif isinstance(self.board[i][j], Modele.Players.machine.Pion):
                        self.liste_piece[i][j] = Piece("pion", self.board[i][j].couleurBlanc, self.board[i][j].position)
        self.nouveau()

    def nouveau(self):
        """
        Met à jour l'apparence du jeu (déselectionne tout ce qui est sélectionné)
        """
        self.screen.fill((0, 0, 0))
        self.echiquier.blit(self.screen)
        self.undo_button.blit(self.screen)
        self.list_button.blit(self.screen)

        for i in self.liste_piece:
            for j in i:
                if j is not None:
                    if j.estVert:
                        j.estVert = False
                    j.blit(self.screen)
        self.liste_vert.clear()

    def init_pieces(self):
        """
        Initialise la self.board avec les pièces au début de chaque partie
        """
        for i in range(4):
            colum_reflechi = 7 - i
            if i == 0:
                self.board[i][0], self.board[colum_reflechi][0] = Tour([i, 0], True), Tour([colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Tour([i, 7], False), Tour([colum_reflechi, 7], False)
            elif i == 1:
                self.board[i][0], self.board[colum_reflechi][0] = Chevalier([i, 0], True), Chevalier(
                    [colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Chevalier([i, 7], False), Chevalier(
                    [colum_reflechi, 7], False)
            elif i == 2:
                self.board[i][0], self.board[colum_reflechi][0] = Fou([i, 0], True), Fou([colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Fou([i, 7], False), Fou([colum_reflechi, 7], False)
            elif i == 3:
                self.board[i][0], self.board[colum_reflechi][0] = Reine([i, 0], True), Roi([colum_reflechi, 0], True)
                self.board[i][7], self.board[colum_reflechi][7] = Reine([i, 7], False), Roi([colum_reflechi, 7], False)
        for i in range(8):
            self.board[i][1] = Modele.Players.machine.Pion([i, 1], True)
            self.board[i][6] = Modele.Players.machine.Pion([i, 6], False)

        ordre = [TypePiece.TOUR,
                 TypePiece.CAVALIER,
                 TypePiece.FOU,
                 TypePiece.REINE,
                 TypePiece.ROI,
                 TypePiece.FOU,
                 TypePiece.CAVALIER,
                 TypePiece.TOUR]
        for i in range(8):
            self.liste_piece[i][0] = Piece(ordre[i].name, True, [i, 0])
            self.liste_piece[i][1] = Piece("pion", True, [i, 1])
            self.liste_piece[i][7] = Piece(ordre[i].name, False, [i, 7])
            self.liste_piece[i][6] = Piece("pion", False, [i, 6])
        for i in self.liste_piece:
            for j in i:
                if j is not None:
                    j.blit(self.screen)

    def mouvementInterface(self, position, lastPosition, move_special):

        """
        Déplace visuellement la pièce sélectionnée (prends en compte les mouvements spéciaux)
        :param position:
        :param lastPosition:
        :param move_special:
        """
        self.liste_piece[position[0]][position[1]] = self.liste_piece[lastPosition[0]][lastPosition[1]]
        self.liste_piece[lastPosition[0]][lastPosition[1]].setPosition(position)
        self.liste_piece[lastPosition[0]][lastPosition[1]] = None

        if move_special == MoveSpecial.PRISE_EN_PASSANT:
            self.liste_piece[position[0]][lastPosition[1]] = None
        elif move_special == MoveSpecial.PROMOTION:
            inputs = ""

            if isinstance(self.board[position[0]][position[1]], Reine):
                inputs = Modele.Players.machine.Pion.getChoices()[0]
            elif isinstance(self.board[position[0]][position[1]], Tour):
                inputs = Modele.Players.machine.Pion.getChoices()[1]
            elif isinstance(self.board[position[0]][position[1]], Fou):
                inputs = Modele.Players.machine.Pion.getChoices()[2]
            elif isinstance(self.board[position[0]][position[1]], Chevalier):
                inputs = Modele.Players.machine.Pion.getChoices()[3]
            tempPiece = Piece(inputs.name, self.liste_piece[position[0]][position[1]].estBlanc, position)
            self.liste_piece[position[0]][position[1]] = tempPiece
        elif move_special == MoveSpecial.ROQUE:
            if lastPosition[0] - position[0] == -2:
                self.liste_piece[position[0] - 1][position[1]] = self.liste_piece[7][position[1]]
                self.liste_piece[position[0] - 1][position[1]].setPosition([position[0] - 1, position[1]])
                self.liste_piece[7][position[1]] = None
            elif lastPosition[0] - position[0] == 2:
                self.liste_piece[position[0] + 1][position[1]] = self.liste_piece[0][position[1]]
                self.liste_piece[position[0] + 1][position[1]].setPosition([position[0] + 1, position[1]])
                self.liste_piece[0][position[1]] = None

        self.boardToInterface()


chess_init = Chess()
chess_init.intro_loop()
chess_init.game_loop()
