import math

class CalculadoraGeografica():
    datum = {
        "nome": "SIRGAS2000",
        "semiEixo": 6.3781370e+06,
        "achatamento": 3.35281068e-03,
        "deltaX": 0.0,
        "deltaY": 0.0,
        "deltaZ": 0.0,
    }

    def getMeridianoCentral(lon):
        zona = math.floor((lon + 180) / 6) + 1
        return (6 * zona) - 183

    def geo_para_utm(self, lat, lon):
        semiEixo = self.datum["semiEixo"]
        achat = self.datum["achatamento"]
        offY = 10000000 if lat < 0 else 0
        lonMc = math.radians(self.getMeridianoCentral(lon))

        lat = math.radians(lat)
        lon = math.radians(lon)

        k0 = 1.0 - (1.0 / 2500.0)
        equad = 2.0 * achat - math.pow(achat, 2.0)
        elinquad = equad / (1.0 - equad)

        aux1 = equad * equad
        aux2 = aux1 * equad
        aux3 = math.sin(2 * lat)
        aux4 = math.sin(4 * lat)
        aux5 = math.sin(6 * lat)
        aux6 = (1.0 - (equad / 4.0) - (3.0 * aux1) / 64.0 - (5.0 * aux2) / 256) * lat
        aux7 = ((3.0 * equad) / 8.0 + (3.0 * aux1) / 32.0 + (45.0 * aux2) / 1024.0) * aux3
        aux8 = ((15.0 * aux1) / 256.0 + (45.0 * aux2) / 1024.0) * aux4
        aux9 = ((35.0 * aux2) / 3072.0) * aux5

        n = semiEixo / math.sqrt(1.0 - equad * math.pow(math.sin(lat), 2.0))
        t = math.pow(math.tan(lat), 2.0)
        c = elinquad * math.pow(math.cos(lat), 2.0)
        ag = (lon - lonMc) * math.cos(lat)
        m = semiEixo * (aux6 - aux7 + aux8 - aux9)

        aux10 = (1.0 - t + c) * math.pow(ag, 3.0) / 6.0
        aux11 = (5.0 - 18.0 * t + t * t + 72.0 * c - 58.0 * elinquad) * math.pow(ag, 5.0) / 120.0
        aux12 = (5.0 - t + 9.0 * c + 4.0 * c * c) * math.pow(ag, 4.0) / 24.0
        aux13 = (61.0 - 58.0 * t + t * t + 600.0 * c - 330.0 * elinquad) * math.pow(ag, 6.0) / 720.0

        x = 500000.0 + k0 * n * (ag + aux10 + aux11)
        y = offY + k0 * (m + n * math.tan(lat) * (math.pow(ag, 2.0) / 2.0 + aux12 + aux13))
        return x, y