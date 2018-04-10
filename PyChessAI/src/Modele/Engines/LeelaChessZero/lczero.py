from Modele.Engines.ucip_engine import UCIP_Engine


class LCZero(UCIP_Engine):
    def __init__(self, couleur, game):
        super().__init__(couleur, None, game, command=['Modele/Engines/LeelaChessZero/lczeroEngine', '-w',
                                                       'Modele/Engines/LeelaChessZero/weights.txt'])
