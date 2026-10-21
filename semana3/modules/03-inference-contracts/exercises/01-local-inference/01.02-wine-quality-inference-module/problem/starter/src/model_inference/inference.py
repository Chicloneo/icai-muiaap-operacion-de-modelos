"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.
import joblib
from pathlib import Path
import json

from .contracts import WineQualityPrediction
from .preprocess import FEATURE_NAMES, PREPROCESSING_VERSION, WineFeatures

CURRENT_DIR = Path(__file__).resolve().parent
# La raíz del proyecto es donde está models y pyproject.toml
PROJECT_ROOT = CURRENT_DIR.parent.parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "wine_quality_classifier.joblib"
MANIFEST_PATH = PROJECT_ROOT / "manifest.json"

def load_manifest(ruta_manifest=MANIFEST_PATH):

    path = Path(ruta_manifest)
    if not path.exists():
        raise ValueError(f"El manifest '{path}' no existe.")

    with open(path,'r') as j:
        manifest = json.load(j)

    return manifest


def load_wine_quality_model(path=DEFAULT_MODEL_PATH):
    """Validamos el modelo antes de devolverlo"""
    manifest = load_manifest()

    path = Path(path)
    if not path.exists():
        raise ValueError(f"El modelo '{path}' no existe.")

    modelo = joblib.load(path)

    if "estimator" not in modelo:
        raise ValueError(f"El modelo no tiene estimador y debe tenerlo. No hay clasificador compatible; falta la clave 'estimator'.")

    if "feature_names" not in modelo:
        raise ValueError(f"El modelo no tiene feature_names y debe tenerlo")

    if "model_version" not in modelo:
        raise ValueError(f"El modelo no tiene model_version y debe tenerlo")

    if modelo.get('feature_names') != FEATURE_NAMES:
        raise ValueError(f"El modelo espera feature_names: {FEATURE_NAMES} pero recibe {modelo['feature_names']}")

    if type(modelo.get("estimator")).__name__ == manifest["estimator_name"]:

        if modelo.get("feature_names") != manifest["feature_names"]:
            raise ValueError("feature_names del modelo y manifest son distintos")

        if modelo.get("model_version")!=manifest["model_version"]:
            raise ValueError("model_version del modelo y del manifest son distintos")


        if type(modelo.get("estimator")).__name__ != manifest["estimator_name"]:
            #esta condición claramente en este caso no se va a cumplir
            #pero lo dejo aquí de momento
            raise ValueError("Nombre del estimador del modelo y del manifest no coinciden")

        if PREPROCESSING_VERSION != manifest["preprocessing_version"]:
            raise ValueError("Versión del preprocesado no coincide con la del manifest")

        model_params = modelo.get("estimator").get_params()
        for param in manifest["estimator_params"]:
            if manifest["estimator_params"][param] != model_params[param]:
                raise ValueError(f"Parámetro {param} del modelo y del manifest no coinciden")
    
    return modelo


def infer_wine_quality(model, fila_preprocesada: WineFeatures) -> WineQualityPrediction:

    fila_preprocesada = fila_preprocesada.as_vector()

    estimator = model["estimator"]
    quality_band = str(estimator.predict([fila_preprocesada])[0])
    confidence = float(max(estimator.predict_proba([fila_preprocesada])[0]))

    return WineQualityPrediction(
        quality_band=quality_band,
        confidence=round(confidence,4), #4 decimales
        model_version=model["model_version"],
        preprocessing_version=PREPROCESSING_VERSION,
    )