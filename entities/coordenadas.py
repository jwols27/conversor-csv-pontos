class Coordenadas:
    def __init__(self, latitude = None, longitude = None):
        self.latitude: float = latitude     # y
        self.longitude: float = longitude   # x

    def get_latitude(self):
        return 0 if self.latitude is None else self.latitude

    def get_longitude(self):
        return 0 if self.longitude is None else self.longitude