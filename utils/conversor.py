import pandas as pd
from pathlib import Path
from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:4674", "EPSG:32722", always_xy=True)
# se Easting e Northing não existirem, usar valores da Longitude e da Latitude convertidos
def converter_para_utm(row):
    if pd.isna(row["Easting"]) and pd.isna(row["Northing"]):
        easting, northing = transformer.transform(
            row["Longitude"], row["Latitude"]
        )
        return easting, northing
    return row["Easting"], row["Northing"]

class ConversorCoordernadas:
    @staticmethod
    def converter(file_path, norte, este, altura):
        df = pd.read_csv(file_path)
        colunas_manter = ["Name", "Northing", "Easting", "Elevation", "Description"]

        df[["Easting", "Northing"]] = df.apply(
            converter_para_utm, axis=1, result_type="expand"
        )

        # se Elevation estiver vazio, preencher com Ellipsoidal height correspondente
        df["Elevation"] = df["Elevation"].fillna(df["Ellipsoidal height"])

        # calcula o valor corrigido
        df["Northing"] -= norte
        df["Easting"] -= este
        df["Elevation"] -= altura

        # mudando para arquivo txt
        arquivo_novo = f'{Path(file_path).parent}/pontos {Path(file_path).stem}.txt'
        df[colunas_manter].to_csv(arquivo_novo, header=None, index=False, sep="\t")
