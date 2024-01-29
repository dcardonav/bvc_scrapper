__author__ = "David Cardona-Vasquez"
__copyright__ = "Copyright 2023, David Cardona-Vasquez"
__credits__ = ["David Cardona-Vasquez"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "David Cardona-Vasquez"
__status__ = "Development"

import datetime
import os
import pandas as pd
import pathlib

raiz = pathlib.Path(os.path.join(os.getcwd(),
                                 "historicos",
                                 "mercado_local"))

columnas = ['Nemotécnico', 'Último precio', 'Variación porcentual', 'Volúmenes', 'Cantidad', 'Variación absoluta',
            'Precio apertura', 'Precio máximo', 'Precio mínimo', 'Precio promedio', 'Emisor / Nombre']
lista_df = []
for f in raiz.rglob("RVLocal_*.csv"):
    aux = pd.read_csv(f, sep=";", decimal=",", skiprows=1, header=None, na_values=['-'])
    if aux.shape[1] != 11:
        try:
            aux.drop(columns=[11], inplace=True)
        except KeyError:
            print(aux.columns)

    fecha = f.name[8:16]
    aux.columns = columnas
    aux['fecha'] = datetime.datetime.strptime(fecha, "%Y%m%d").date()
    lista_df.append(aux.copy())

df_completo = pd.concat(lista_df)
df_completo.to_excel(r"historicos\historico_2010_2023.xlsx", index=False)
df_completo.to_csv(r"historicos\historico_2010_2023.csv", index=False, sep=';')





