import joblib

from app.config import MODEL_PATH
from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada

# Orden en el que el modelo espera las variables
VARIABLES = [
    "edad",
    "ingresos_mensuales",
    "importe_prestamo",
    "plazo_meses",
    "antiguedad_laboral_anios",
    "impagos_previos",
]

# TODO: cargar el modelo joblib una sola vez, al importar el modulo

def load_model():
    return joblib.load(MODEL_PATH)

MODELO = load_model()

# TODO: funcion decidir(probabilidad) -> "aprobar", "revisar" o "rechazar" (umbrales en el enunciado)

def decidir(probabilidad):
    if probabilidad < 0.2:
        return "aprobar"
    elif probabilidad < 0.5:
        return "revisar"
    else:
        return "rechazar"


# TODO: funcion predecir(entrada) -> PrediccionSalida, usando VARIABLES para ordenar los valores

def predecir(entrada: PrestamoEntrada):

    diccionario_entrada = list(entrada.model_dump())

    #Explicación de esta línea en el notebook
    probabilidad_impago = MODELO.predict_proba([diccionario_entrada[i] for i in VARIABLES])[0][1]

    decision = decidir(probabilidad_impago)

    return PrediccionSalida(
        probabilidad_impago=probabilidad_impago,
        decision=decision
    )
