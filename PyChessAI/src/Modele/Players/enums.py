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
    MOUVEMENT_TOUR = 3
    PREMIER_MOUVEMENT_ROI = 4
    PREMIER_MOUVEMENT_PION = 5
    PRISE_EN_PASSANT_IMPOSSIBLE = 6

