import pgn
from Modele.Elements.chevalier import Chevalier
from Modele.Elements.fou import Fou
from Modele.Elements.pion import Pion
from Modele.Elements.pieceM import PieceM
from Modele.Elements.reine import Reine
from Modele.Elements.roi import Roi
from Modele.Elements.tour import Tour
from Modele.Players.enums import ChessNotation
from Modele.Players.enums import PieceChess


#10009

class ParsePgn():
    def __init__(self, file_name):
        pgn_text = open(file_name + ".pgn").read()
        self.games = pgn.loads(pgn_text)
        self.board = None
        self.initPiece()
        self.tourBlanc = None
        self.promotedPiece = None
    '''
    def afficher(self):
        for i in self.board:
            message = ""
            for j in i:
                printer = 0
                if j is None:
                    message += str(PieceChess.NONE.value)
                    printer = 1
                else:
                    multiplier = -1
                    printer = 0
                    if j.couleurBlanc:
                        multiplier = 1
                        printer = 1

                    if isinstance(j, Pion):
                        message += str(PieceChess.PION.value * multiplier)
                    elif isinstance(j, Chevalier):
                        message += str(PieceChess.CAVALIER.value * multiplier)
                    elif isinstance(j, Fou):
                        message += str(PieceChess.FOU.value * multiplier)
                    elif isinstance(j, Tour):
                        message += str(PieceChess.TOUR.value * multiplier)
                    elif isinstance(j, Reine):
                        message += str(PieceChess.REINE.value * multiplier)
                    elif isinstance(j, Roi):
                        message += str(PieceChess.ROI.value * multiplier)
                message += " " + " "*printer
            print(message)
        print("\n")
    '''

    #remplir le board pour que celui-ci devienne un board qui n'a pas encore été touché
    def initPiece(self):
        self.tourBlanc = True
        self.board = [[None for _ in range(8)] for _ in range(8)]
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
            self.board[i][1] = Pion([i, 1], True)
            self.board[i][6] = Pion([i, 6], False)

    #create a txt file that has all the moves in this format int[int[], int[]] -> [lastPosition, position]
    def createFile(self):
        for game in self.games:
            self.initPiece()
            partie = game.moves[:len(game.moves)-2]
            temp = []
            for string in partie:
                #self.afficher()
                infos = self.parserInfo(string)
                temp.append(infos)
                self.mouvementMemory(infos[0], infos[1])
                self.tourBlanc = not self.tourBlanc
            print("done")
            #fichier = open("data.txt", "a")
            #fichier.write("\n" + str(temp))
            #fichier.close()
        print("succ")

    # va faire le changement plus complet que testMouvementMemory dans le sens ou il va tenir en compte de savoir s'il y a un coup special
    def mouvementMemory(self, lastPosition, position):
        if isinstance(self.board[lastPosition[0]][lastPosition[1]], Pion):
            self.board[lastPosition[0]][lastPosition[1]].ongoingPassant(position, lastPosition, self.board)

        self.board[position[0]][position[1]] = self.board[lastPosition[0]][lastPosition[1]]
        self.board[position[0]][position[1]].position = position
        self.board[lastPosition[0]][lastPosition[1]] = None

        self.board[position[0]][position[1]].prisePassant(lastPosition, self.board)

        if isinstance(self.board[position[0]][position[1]], Pion):
            if position[1] == 7 or position[1] == 0:
                output = self.tradPiece(position)
                self.promotedPiece = None
                self.board[position[0]][position[1]].promotion(output, self.board)
        elif isinstance(self.board[position[0]][position[1]], Tour):
            if not (self.board[position[0]][position[1]].moved):
                self.board[position[0]][position[1]].moved = True
        elif isinstance(self.board[position[0]][position[1]], Roi):
            if not self.board[position[0]][position[1]].moved:
                if lastPosition[0] - position[0] == -2:
                    self.board[7][position[1]].mouvementMemory([position[0] - 1, position[1]], [7, position[1]], self.board)
                elif lastPosition[0] - position[0] == 2:
                    self.board[0][position[1]].mouvementMemory([position[0] + 1, position[1]], [0, position[1]], self.board)
                self.board[position[0]][position[1]].moved = True

    #faire en sorte de ouput le string de promotion
    def tradPiece(self, position):
        if self.promotedPiece == ChessNotation.DAME.value:
            return Pion.getChoices()[0]
        elif self.promotedPiece == ChessNotation.TOUR.value:
            return Pion.getChoices()[1]
        elif self.promotedPiece == ChessNotation.FOU.value:
            return Pion.getChoices()[2]
        return Pion.getChoices()[3]


    #transformer le string du mouvement avec le bard en mouvement -> basically le parser
    #va return un int[int[], int[]]
    def parserInfo(self, string):
        lastPosition = []
        position = []
        if string[-1] == ChessNotation.MAT.value: #mat
            string = string[:len(string)-1]
        elif string[-1] == ChessNotation.ECHEC.value: #échec
            string = string[:len(string)-1]


        if string == ChessNotation.PETITROQUE.value:
            posRoi = PieceM.trouverRoi(self.board, self.tourBlanc)
            position, lastPosition = [posRoi[0]+2, posRoi[1]], posRoi
        elif string == ChessNotation.GRANDROQUE.value:
            posRoi = PieceM.trouverRoi(self.board, self.tourBlanc)
            position, lastPosition = [posRoi[0]-2, posRoi[1]], posRoi
        elif ChessNotation.PROMOTION.value in string:
            string, self.promotedPiece = string.split(ChessNotation.PROMOTION.value)[0], string.split(ChessNotation.PROMOTION.value)[1]
            if ChessNotation.MANGER.value in string:
                initial, final = string.split(ChessNotation.MANGER.value)
                y_final = int(final[-1]) -1
                y_initial = 1
                if y_final == 7:
                    y_initial = 6

                lastPosition = [int(ord(initial)) - int(ord('a')), y_initial]
                position = [int(ord(final[0])) - int(ord('a')), y_final]
            else:
                x_deux = int(ord(string[0])) - int(ord('a'))
                if int(string[1])-1 == 7:
                    lastPosition = [x_deux, 6]
                    position = [x_deux, 7]
                else:
                    lastPosition = [x_deux, 1]
                    position = [x_deux, 0]
        else:
            reste, position = string[0: len(string) - 2], [int(ord(string[-2])) - int(ord('a')), int(string[-1]) - 1]
            if len(reste) == 0: # déplacement d'un pion sans capture
                opposeVitesse = -1 if self.tourBlanc else 1
                lastPosition = [position[0], position[1] + opposeVitesse] if isinstance(self.board[position[0]][position[1] + opposeVitesse], Pion) else [position[0], position[1] + 2*opposeVitesse]
            elif len(reste) == 4: #Qa1x (dans le cas où on a 3 dames -> va presque jamais rentrer dans ça)
                string = string[1:3]
                lastPosition = [int(ord(string[0])) - int(ord('a')), int(string[1])]
            else:
                premier = reste[0]
                string = reste[1:]
                if int(ord(premier)) > int(ord('Z')): # sa veut dire que c'est un pion qui a mangé quelque chose et le premier représente la lettre en x
                    opposeVitesse = -1 if self.tourBlanc else 1
                    lastPosition = [int(ord(premier))-int(ord('a')), position[1] + opposeVitesse]
                else: # c'est une autre piece qui a fait qqlqchose string peut avoir un ex: '' ou 'x' ou 'ax' '3x' ou 'b'
                    pieces = self.findPiece(premier, position)
                    if len(pieces) == 1: # juste une piece qui aurait pu faire le mouvement
                        lastPosition = pieces[0].position
                    elif len(string) == 0 or len(string) == 1: #c'est de format '' ou 'x'
                        if len(string) == 0 or string == ChessNotation.MANGER.value:
                            for temp in pieces:
                                moves = temp.possibiliteBouger(self.board)
                                if moves[position[0]][position[1]]:
                                    lastPosition = temp.position
                        elif int(ord(string)) < int(ord('a')) : #c'est un nombre
                            for temp in pieces:
                                if temp.position[1] == int(string)-1:
                                    lastPosition = temp.position
                        else:
                            for temp in pieces:
                                if temp.position[0] == int(ord(string)) - int(ord('a')):
                                    lastPosition = temp.position
                    elif len(string) == 2: # le string est de format 'ax' ou '3x'
                        string = string[0]
                        if int(ord(string)) < int(ord('A')) : # est ce que c'est un nombre
                            for i in pieces:
                                if i.position[1] == int(string)-1:
                                    lastPosition = i.position
                        else:
                            valeurNumeric = int(ord(string)) - int(ord('a'))
                            for i in pieces:
                                if i.position[0] == valeurNumeric:
                                    lastPosition = i.position
        if len(lastPosition) != 2:
            print("sndklad")

        return [lastPosition, position]


    #cela exclut les pions (pcq on a pas besoin de les faire)
    def findPiece(self, string, position):
        piece = []
        typePiece = None
        if string == ChessNotation.ROI.value:
            typePiece = Roi
        elif string == ChessNotation.DAME.value:
            typePiece = Reine
        elif string == ChessNotation.TOUR.value:
            typePiece = Tour
        elif string == ChessNotation.FOU.value:
            typePiece = Fou
        elif string == ChessNotation.CAVALIER.value:
            typePiece = Chevalier
        else:
            return None

        for i in self.board:
            for j in i:
                if j != None and j.couleurBlanc == self.tourBlanc and isinstance(j, typePiece):
                    moves = j.possibiliteBouger(self.board)
                    posRoi = PieceM.trouverRoi(self.board, self.tourBlanc)
                    self.board[posRoi[0]][posRoi[1]].acceptableMove(moves, self.board, j.position)
                    if moves[position[0]][position[1]]:
                        piece.append(j)
        return piece


lol = ParsePgn("setGames1")
lol.createFile()
