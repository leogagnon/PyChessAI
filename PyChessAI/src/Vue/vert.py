from Vue.image import Image
class Vert(Image):
    def __init__(self, coordonnees):
        super().__init__('vert',initImage=True)
        self.coordonnees = coordonnees
        self.position = [coordonnees[0] * self.dimension_case + self.bottom_left[0], -(self.coordonnees[1] + 1) * self.dimension_case + self.bottom_left[1]]


