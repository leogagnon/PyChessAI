from enum import Enum

class ModeDeJeu(Enum):
    JOUEUR_JOUEUR = 0
    JOUEUR_MACHINE = 1
    MACHINE_MACHINE = 2

class TypePiece(Enum):
    CAVALIER = 'cavalier'
    FOU = 'fou'
    PION = 'pion'
    REINE = 'reine'
    ROI = 'roi'
    TOUR = 'tour'

class MoveSpecial(Enum):
    NULL = -1
    PRISE_EN_PASSANT = 0
    PROMOTION = 1
    ROQUE = 2
    PREMIER_MOUVEMENT_TOUR = 3
    PREMIER_MOUVEMENT_ROI = 4
    PREMIER_MOUVEMENT_PION = 5
    PRISE_EN_PASSANT_IMPOSSIBLE = 6

class ChessNotation(Enum):
    ROI = "K"
    DAME = "Q"
    TOUR = "R"
    FOU = "B"
    CAVALIER = "N"
    ECHEC = "+"
    MAT = "#"
    PETITROQUE = "O-O"
    GRANDROQUE = "O-O-O"
    MANGER = "x"
    PROMOTION = "="

class PieceChess(Enum):
    NONE = 0
    PION = 1
    CAVALIER = 2
    FOU = 3
    TOUR = 4
    REINE = 5
    ROI = 6



