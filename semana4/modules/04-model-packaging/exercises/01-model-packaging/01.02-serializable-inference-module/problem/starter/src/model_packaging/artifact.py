"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
from pydantic import BaseModel, ConfigDict, Field

from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)

from .preprocess import FEATURE_NAMES, PREPROCESSING_VERSION

ARTIFACT_SCHEMA_VERSION = "wine-quality-bundle-v1"
DEFAULT_BUNDLE_PATH = Path("models/wine_quality_bundle")
MANIFEST_FILENAME = "manifest.json"
MODEL_FILENAME = "model.joblib"
OUTPUT_LABELS: tuple[QualityBand, ...] = (
    "needs_review",
    "acceptable",
    "excellent",
)


class WineQualityEstimator(Protocol):
    """Interfaz mínima que debe cumplir el estimador cargado."""

    def predict(self, features: list[list[float]]) -> Sequence[str]:
        """Devuelve una etiqueta por fila."""

    def predict_proba(self, features: list[list[float]]) -> Sequence[Sequence[float]]:
        """Devuelve probabilidades por fila."""


class ArtifactManifest(BaseModel):
    """TODO: declara y valida los metadatos del bundle."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    preprocessing_version: str = Field(min_length=1)
    feature_names: tuple[str, ...]
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)


@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest


def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """TODO: devuelve un manifiesto compatible con el contrato."""

    return ArtifactManifest(
        schema_version=ARTIFACT_SCHEMA_VERSION,
        model_version=model_version,
        preprocessing_version=PREPROCESSING_VERSION,
        feature_names=FEATURE_NAMES,
        output_labels=OUTPUT_LABELS,
        estimator_type=type(estimator).__name__,
    )


def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,
    manifest: ArtifactManifest | None = None,
) -> ArtifactManifest:
    """TODO: escribe manifest.json y model.joblib de forma segura."""

    dir = Path(bundle_path)
    dir.mkdir(parents=True, exist_ok=True) #lo crea si no existe

    manifest_path = bundle_path / MANIFEST_FILENAME
    manifest_path.write_text(json.dumps(manifest.model_dump(mode="json")))

    model_path = dir / MODEL_FILENAME
    joblib.dump(estimator, model_path) #lo serializamos

    return manifest


def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """TODO: valida el manifiesto antes de cargar el estimador."""

    with open(bundle_path / MANIFEST_FILENAME, 'r') as j:
        manifest = json.load(j)

    try:
        ArtifactManifest.model_validate(manifest)
    except:
        raise ValueError("Manifesto no validado")

    if manifest.get('schema_version') != ARTIFACT_SCHEMA_VERSION:
        raise ValueError(f"No coinciden las schema_version")

    if manifest.get('preprocessing_version') != PREPROCESSING_VERSION:
        raise ValueError(f"No coinciden las preprocessing version")

    if manifest.get('feature_names') != list(FEATURE_NAMES):
        raise ValueError(f"No coinciden las feature_names")

    if manifest.get('output_labels') != list(OUTPUT_LABELS):
        raise ValueError(f"No coinciden las output labels")

    arti_mani = ArtifactManifest(
        schema_version=manifest.get('schema_version'),
        model_version=manifest.get("model_version"),
        preprocessing_version=manifest.get('preprocessing_version'),
        feature_names = manifest.get("feature_names"),
        output_labels = manifest.get('output_labels'),
        estimator_type = manifest.get('estimator_type')
    )

    estim = joblib.load(bundle_path / MODEL_FILENAME)

    if isinstance(estim, dict) and "estimator" in estim:
        estim = estim["estimator"]

    if not callable(getattr(estim, "predict", None)):
        raise ValueError("El bundle no contiene un estimador válido.")

    return LoadedModelBundle(
        estimator = estim,
        manifest = arti_mani
    )


def infer_wine_quality(
    bundle: LoadedModelBundle,
    request: WineQualityRequest,
) -> WineQualityPrediction:
    """TODO: preprocesa, invoca el estimador y valida la respuesta."""

    estimator = bundle.estimator
    manifest = bundle.manifest

    feature_vector = [request.model_dump()[name] for name in FEATURE_NAMES]
    labels = estimator.predict([feature_vector])

    if labels[0] not in manifest.output_labels:
        raise ValueError(f"{labels[0]} no es válido como etiqueta de salida")
    
    probabilities = estimator.predict_proba([feature_vector])

    predicted_label = labels[0]
    class_labels = list(estimator.classes_)
    predicted_index = class_labels.index(predicted_label)
    confidence = float(probabilities[0][predicted_index])

    return WineQualityPrediction(
        quality_band=labels[0],
        confidence=confidence,
        preprocessing_version=manifest.preprocessing_version,
        model_version = manifest.model_version
    )


