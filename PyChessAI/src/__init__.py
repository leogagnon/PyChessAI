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
from Modele.Game.machine import TypeEngine
from Modele.Game.game import Game
from Vue.bouton import Bouton
from Vue.image import Image
from Modele.Game.humain import Humain
from Modele.Game.enums import ModeDeJeu, TypePiece, MoveSpecial
import easygui
import sys
import easygui_qt


class Chess():
    def __init__(self):

        """
        Constructeur : Initialisations des différents éléments nécéssaires au jeu
        """
        # Déclaration des différentes images
        self.echiquier = Image('echiquier', [0, 0])
        self.undo_button = Bouton('undo', [self.echiquier.dimension[0] + 25, 125 + 40 * 5])
        self.list_button = Bouton('list-moves', [self.echiquier.dimension[1] + 25, 125 + 40 * 4])

        # Déclaration des tableaux
        self.liste_piece = [[None for _ in range(8)] for _ in range(8)]
        self.liste_vert = []
        self.position_curseur = []
        self.lastPosition = [0, 0]

        # La partie
        self.game = None

        # Initialisation de la fenetre de PyGame
        self.init_pygame()

    def game_loop(self):
        """
        Fonctionnement logique de la partie
        """
        self.echiquier.blit(self.screen)
        self.init_pieces()
        if self.game.mode_de_jeu is not ModeDeJeu.MACHINE_MACHINE:
            self.undo_button.blit(self.screen)
            self.list_button.blit(self.screen)

        pygame.display.flip()

        # Indique si la partie est terminée
        done = False

        # Boucle principale
        while not done:
            if isinstance(self.game.get_active_player(), Humain):
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

                        if pieceTemp is not None and (self.game.tour_blanc == pieceTemp.estBlanc or pieceTemp.estVert):
                            self.clicked(pieceTemp)
                            done = self.check_mat()
                        vert = None
                        for temp in self.liste_vert:
                            if temp.image.get_rect().move(temp.position[0], temp.position[1]).collidepoint(
                                    self.position_curseur):
                                vert = temp

                        if vert is not None:
                            self.clickedVert(vert)
                            done = self.check_mat()
                            self.boardToInterface()
                            # si on clique sur le boutton undo (commentaire pour le if suivant)
                        elif self.game.memoire.numero_move != 0 and self.undo_button.image.get_rect().move(
                                self.undo_button.position[0], self.undo_button.position[1]).collidepoint(
                            self.position_curseur):
                            if self.game.mode_de_jeu == ModeDeJeu.JOUEUR_JOUEUR:
                                self.game.undo()
                            else:
                                self.game.undo()
                                self.game.undo()
                            self.boardToInterface()
                        elif self.list_button.image.get_rect().move(self.list_button.position[0],
                                                                    self.list_button.position[1]).collidepoint(
                            self.position_curseur):

                            liste_moves = ''

                            for i in self.game.memoire.tous_move:
                                liste_moves += i + '\n'

                            easygui_qt.show_message(liste_moves,'Liste des moves')



            else:
                #pygame.time.wait(1000)
                self.game.next()
                done = self.check_mat()
                self.boardToInterface()

            pygame.display.flip()

        restart = self.demandeQuitter()
        if restart:
            chess_init = Chess()
            chess_init.intro_loop()
            chess_init.game_loop()

    def demandeQuitter(self):
        options = ["Recommencer", "Quitter"]
        msg = "Voulez-vous recommencer? "
        titre = "Fin"
        choix = easygui_qt.get_choice(msg, titre, options)

        if choix == options[0]:
            return True
        elif choix == options[1]:
            return False


    def check_mat(self):
        posRoi = PieceM.trouverRoi(self.game.board, self.game.tour_blanc)
        if self.game.board[posRoi[0]][posRoi[1]].mat(self.game.board):
            return True
        return False

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

        # Boucle principale
        while self.game is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.position_curseur = pygame.mouse.get_pos()

                    if HH_button.image.get_rect().move(HH_button.position[0], HH_button.position[1]).collidepoint(
                            self.position_curseur):
                        self.init_game(ModeDeJeu.JOUEUR_JOUEUR)
                    elif HM_button.image.get_rect().move(HM_button.position[0], HM_button.position[1]).collidepoint(
                            self.position_curseur):
                        self.init_game(ModeDeJeu.JOUEUR_MACHINE)
                    elif MM_button.image.get_rect().move(MM_button.position[0], MM_button.position[1]).collidepoint(
                            self.position_curseur):
                        self.init_game(ModeDeJeu.MACHINE_MACHINE)

        self.screen.fill((0, 0, 0))

    def init_game(self, mode_de_jeu):

        """
        Dialogue permettant d'initialiser la partie
        :param mode_de_jeu: Mode de jeu choisi
        """
        if mode_de_jeu is ModeDeJeu.JOUEUR_JOUEUR:

            self.game = Game(ModeDeJeu.JOUEUR_JOUEUR)

        elif mode_de_jeu is ModeDeJeu.JOUEUR_MACHINE:
            ai = self.choix_AI('Engine : ')
            depth = self.choix_depth(ai)
            blanc = self.choix_couleur()

            self.game = Game(ModeDeJeu.JOUEUR_MACHINE, choix_couleur=blanc, AI_1=ai, depth_1=depth)
        elif mode_de_jeu is ModeDeJeu.MACHINE_MACHINE:
            ai_1 = self.choix_AI('Engine 1 (Blancs): ')
            depth_1 = self.choix_depth(ai_1)
            ai_2 = self.choix_AI('Engine 2 (Noirs): ')
            depth_2 = self.choix_depth(ai_2)

            self.game = Game(ModeDeJeu.MACHINE_MACHINE, AI_1=ai_1, depth_1=depth_1, AI_2=ai_2, depth_2=depth_2)

    def choix_couleur(self):

        """
        Demande à l'utilisateur s'il veux commencer
        :return: True si il veux commencer, False si il ne veux pas commencer et None pour Cancel
        """
        return easygui_qt.get_yes_or_no(message='Voulez-vous commencer? (Blancs)', title='Choix de couleur')

    def choix_AI(self, message):
        """
        Demande à l'utilisateur de choisir un engine
        :param message: Message envoyé à l'utilisateur
        :return: Enum ModeDeJeu correspondant au type d'engine choisi
        """
        choix = []
        for i in TypeEngine:
            choix.append(i.value)

        reponse = easygui_qt.get_choice(message, choices=choix)

        for i in TypeEngine:
            if reponse == i.value:
                return i

    def choix_depth(self, ai):
        """
        Demande à l'utilisateur de choisir la profondeur d'évaluation
        :param ai: Engine utilisée
        :return:
        """
        depth = None
        if ai is TypeEngine.ALPHA_BETA:
            depth = easygui_qt.get_int(message='Profondeur d\'évaluation : ', title='Depth', default_value=2, min_=1,
                                       max_=5)
        elif ai is TypeEngine.STOCKFISH:
            depth = easygui_qt.get_int(message='Profondeur d\'évaluation : ', title='Depth', default_value=10, min_=1,
                                       max_=20)
        return depth

    def clickedVert(self, vert):
        """
        Déplace la pièce séclectionnée sur la case verte sélectionnée
        :param vert: Objet Vert sur lequel le joueur clique
        """
        coordonnees = vert.coordonnees[:]
        self.game.move(coordonnees, self.lastPosition)

    def clicked(self, piece):
        """
        Offre les coups possibles au joueur lorsqu'il sélectionne une pièce
        :param piece: Pièce sélectionnée
        """
        coordonnees = piece.coordonnees[:]
        if piece.estVert:
            self.game.move(coordonnees, self.lastPosition)
            self.boardToInterface()
        else:
            self.nouveau()
            moves = self.game.board[coordonnees[0]][coordonnees[1]].possibiliteBouger(self.game.board)
            posRoi = PieceM.trouverRoi(self.game.board, self.game.board[coordonnees[0]][coordonnees[1]].couleurBlanc)
            self.game.board[posRoi[0]][posRoi[1]].acceptableMove(moves, self.game.board, coordonnees)

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

        for i in range(len(self.game.board)):
            for j in range(len(self.game.board[i])):
                if self.game.board[i][j] is not None:
                    if isinstance(self.game.board[i][j], Roi):
                        self.liste_piece[i][j] = Piece("roi", self.game.board[i][j].couleurBlanc,
                                                       self.game.board[i][j].position)
                    elif isinstance(self.game.board[i][j], Reine):
                        self.liste_piece[i][j] = Piece("reine", self.game.board[i][j].couleurBlanc,
                                                       self.game.board[i][j].position)
                    elif isinstance(self.game.board[i][j], Tour):
                        self.liste_piece[i][j] = Piece("tour", self.game.board[i][j].couleurBlanc,
                                                       self.game.board[i][j].position)
                    elif isinstance(self.game.board[i][j], Fou):
                        self.liste_piece[i][j] = Piece("fou", self.game.board[i][j].couleurBlanc,
                                                       self.game.board[i][j].position)
                    elif isinstance(self.game.board[i][j], Chevalier):
                        self.liste_piece[i][j] = Piece("cavalier", self.game.board[i][j].couleurBlanc,
                                                       self.game.board[i][j].position)
                    elif isinstance(self.game.board[i][j], Pion):
                        self.liste_piece[i][j] = Piece("pion", self.game.board[i][j].couleurBlanc,
                                                       self.game.board[i][j].position)
        self.nouveau()

    def nouveau(self):
        """
        Met à jour l'apparence du jeu (déselectionne tout ce qui est sélectionné)
        """
        self.screen.fill((0, 0, 0))
        self.echiquier.blit(self.screen)
        if self.game.mode_de_jeu is not ModeDeJeu.MACHINE_MACHINE:
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
                self.game.board[i][0], self.game.board[colum_reflechi][0] = Tour([i, 0], True), Tour(
                    [colum_reflechi, 0], True)
                self.game.board[i][7], self.game.board[colum_reflechi][7] = Tour([i, 7], False), Tour(
                    [colum_reflechi, 7], False)
            elif i == 1:
                self.game.board[i][0], self.game.board[colum_reflechi][0] = Chevalier([i, 0], True), Chevalier(
                    [colum_reflechi, 0], True)
                self.game.board[i][7], self.game.board[colum_reflechi][7] = Chevalier([i, 7], False), Chevalier(
                    [colum_reflechi, 7], False)
            elif i == 2:
                self.game.board[i][0], self.game.board[colum_reflechi][0] = Fou([i, 0], True), Fou([colum_reflechi, 0],
                                                                                                   True)
                self.game.board[i][7], self.game.board[colum_reflechi][7] = Fou([i, 7], False), Fou([colum_reflechi, 7],
                                                                                                    False)
            elif i == 3:
                self.game.board[i][0], self.game.board[colum_reflechi][0] = Reine([i, 0], True), Roi(
                    [colum_reflechi, 0], True)
                self.game.board[i][7], self.game.board[colum_reflechi][7] = Reine([i, 7], False), Roi(
                    [colum_reflechi, 7], False)
        for i in range(8):
            self.game.board[i][1] = Modele.Elements.pion.Pion([i, 1], True)
            self.game.board[i][6] = Modele.Elements.pion.Pion([i, 6], False)

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

            if isinstance(self.game.board[position[0]][position[1]], Reine):
                inputs = Modele.Game.machine.Pion.getChoices()[0]
            elif isinstance(self.game.board[position[0]][position[1]], Tour):
                inputs = Modele.Game.machine.Pion.getChoices()[1]
            elif isinstance(self.game.board[position[0]][position[1]], Fou):
                inputs = Modele.Game.machine.Pion.getChoices()[2]
            elif isinstance(self.game.board[position[0]][position[1]], Chevalier):
                inputs = Modele.Game.machine.Pion.getChoices()[3]
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