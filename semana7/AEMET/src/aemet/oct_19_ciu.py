import requests
import pandas as pd
from pandas import DataFrame
from pathlib import Path

SERVER = "https://opendata.aemet.es/opendata"

HEADERS = {
    "api_key" : "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYW50aWFnb2xpbGxvbWFjaWFzQGdtYWlsLmNvbSIsImp0aSI6ImJmNjZkMDVmLWY5ODgtNDA2Zi04NjBlLTk5YjJmYjUwYTg1NSIsImV4cCI6MTgwMTI0ODg2NywiaXNzIjoiQUVNRVQiLCJpYXQiOjE3OTI2MDg4NjcsInVzZXJJZCI6ImJmNjZkMDVmLWY5ODgtNDA2Zi04NjBlLTk5YjJmYjUwYTg1NSIsInJvbGUiOiIifQ.sq4eDbdZtCob9SUqoYj9DSxvSpAD2X7t7wAAo3YAhok"
}

ENDPOINT_CLIMATOLOGIAS_DIARIAS = (
    f"{SERVER}/api/valores/climatologicos/diarios/datos/"
    "fechaini/{fechaini}/fechafin/{fechafin}/estacion/{idema}"
)
#la api no recibe parámetros como query params, sino en la propia url

MAIN_DIR = Path(__file__).resolve().parent
# Raíz del proyecto: 'AEMET'
PROJECT_ROOT = MAIN_DIR.parent.parent
OUTPUT_PATH = PROJECT_ROOT / ".tmp" / "oct_19_ciu.csv"
# Crear '.tmp/' si no existe
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def sacar_idema(inventario_estaciones:list) -> str:

    df_estaciones = pd.DataFrame(inventario_estaciones)
    fila_ciu = df_estaciones.loc[df_estaciones["nombre"] == "MADRID, CIUDAD UNIVERSITARIA"]
    indicativo = list(fila_ciu["indicativo"])[0]
    idema = indicativo #es lo mismo

    return idema


def obtener_idema():

    # como el request solo devuelve links, después hay que hacer otro request
    url_inventario = requests.get(
    "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones",
    headers=HEADERS
    ).json().get("datos")


    #devuelve una lista de las estaciones
    inventario_estaciones = requests.get(
        url=url_inventario,
        headers=HEADERS
        ).json()

    idema = sacar_idema(inventario_estaciones=inventario_estaciones)

    return idema


def clima_ciu_octubre(path_params:dict) -> DataFrame:

    path_params["idema"] = obtener_idema()

    url_ciu = ENDPOINT_CLIMATOLOGIAS_DIARIAS.format(**path_params)

    #no devuelve los datos como tal, sino un link.
    #al igual que en obtener_idema(), hay que realizar otro request
    link_datos = requests.get(url=url_ciu, headers=HEADERS).json().get("datos")
    datos_octubre_ciu = requests.get(url=link_datos, headers=HEADERS).json()

    df_ciu_octubre = DataFrame(datos_octubre_ciu)

    return df_ciu_octubre


def main():

    path_params = {
    "fechaini": "2019-10-01T00:00:00UTC",
    "fechafin": "2019-10-31T23:59:59UTC",
    }
    
    df = clima_ciu_octubre(path_params=path_params)

    df.to_csv(OUTPUT_PATH,index=False)


if __name__ == "__main__":
    main()
