import pandas as pd
from pyproj import Transformer

class ConversorCoordernadas():
    def converter(self, filePath, norte, este, altura):
        transformer = Transformer.from_crs("EPSG:4674", "EPSG:32722", always_xy=True)

        def converter_para_utm(lon, lat):
            easting, northing = transformer.transform(lon, lat)
            return easting, northing

        df = pd.read_csv(filePath)
        manter = ['Name', 'Northing', 'Easting', 'Elevation', 'Description']

        df[['Easting', 'Northing']] = df.apply(
            lambda row: converter_para_utm(row['Longitude'], row['Latitude']), axis=1, result_type='expand'
        )

        df['Elevation'] = df["Elevation"].fillna(df["Ellipsoidal height"])

        df['Northing'] -= norte
        df['Easting'] -= este
        df['Elevation'] -= altura

        novo = filePath.replace(".csv", ".txt")
        df[manter].to_csv(novo, header=None, index=False, sep ='\t')
