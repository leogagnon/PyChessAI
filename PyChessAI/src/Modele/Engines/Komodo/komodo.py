from Modele.Engines.ucip_engine import UCIP_Engine


class Komodo(UCIP_Engine):
    def __init__(self, couleur, depth, game):
        super().__init__(couleur, depth, game, command=['Modele/Engines/Komodo/komodoEngine'])
