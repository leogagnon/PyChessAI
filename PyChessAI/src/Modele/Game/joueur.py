from abc import ABC, abstractmethod  # pour faire des classes et des méthodes abstraites
import Modele


#C'est la classe qui va contenir les informations générales que le Engines ou le joueur Humain doivent posséder
class Joueur(ABC):
    # constructeur
    def __init__(self, couleur_blanc):
        self.COULEUR_BLANC = couleur_blanc

    @abstractmethod
    def get_promotion(self):
        pass

