"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.
import joblib

from .contracts import WineQualityPrediction
from .preprocess import FEATURE_NAMES, PREPROCESSING_VERSION

DEFAULT_MODEL_PATH = "src/model_inference/wine_quality_classifier.joblib"


def load_wine_quality_model(path=DEFAULT_MODEL_PATH):
    return joblib.load(path)


def infer_wine_quality(model, fila_preprocesada: list[float]) -> WineQualityPrediction:
    if model['feature_names'] != FEATURE_NAMES:
        raise ValueError(f"El modelo espera {FEATURE_NAMES} pero recibe {model['feature_names']}")

    estimator = model["estimator"]
    quality_band = str(estimator.predict([fila_preprocesada])[0])
    confidence = float(max(estimator.predict_proba([fila_preprocesada])[0]))

    return WineQualityPrediction(
        quality_band=quality_band,
        confidence=confidence,
        model_version=model["model_version"],
        preprocessing_version=PREPROCESSING_VERSION,
    )