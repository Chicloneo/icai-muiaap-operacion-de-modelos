"""TODO: transformación de una muestra validada en el vector del modelo."""
from contracts import WineQualityRequest

PREPROCESSING_VERSION = "wine-red-features-v1"

# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.
FEATURE_NAMES = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
]

# Porque lo pide así el enunciado y los test

class WineFeatures:
    def __init__(self, vector: list[float]):
        self._vector = vector

    def as_vector(self) -> list[float]:
        return self._vector

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.

def preprocess_wine_request(wine_request: WineQualityRequest) -> WineFeatures:
   return WineFeatures([getattr(wine_request, name) for name in FEATURE_NAMES]) #mantenemos el orden

"""
wine_request.name for name in FEATURE_NAMES no funcionaría porque name es un string
Habría que ir uno a uno wine_request.fixed_acidity, wine_request.volatile_acidity, etc.
"""