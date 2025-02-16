from utils import CalculadoraGeografica

class BaseLevantamento:
    def __init__(self, norte = None, este = None, altura = None):
        self.norte: float = norte   # y
        self.este: float = este     # x
        self.altura: float = altura

    def get_norte(self):
        return 0 if self.norte is None else self.norte

    def get_este(self):
        return 0 if self.este is None else self.este

    def get_altura(self):
        return 0 if self.altura is None else self.altura

class BaseLevantada(BaseLevantamento):
    def calcular_coordenadas(self, lat, lon):
        calc = CalculadoraGeografica()
        x, y = calc.geo_para_utm(lat, lon)
        self.norte = y
        self.este = x