"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, overload

from pydantic import BaseModel, ConfigDict, Field, field_validator

from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)

from src.model_packaging.preprocess import PREPROCESSING_VERSION, FEATURE_NAMES

import json

ARTIFACT_SCHEMA_VERSION = "wine-quality-bundle-v1" #variables globales
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

@overload
def test_validator(field:str):
    print("test")

@test_validator # <------- se ejecuta esta función primero siempre que llame a continuacion_de_test_validator
def continuacion_de_test_validator(field:str):
    print(field)



class ArtifactManifest(BaseModel): #BaseModel hace que ArtifactManifest sea una clase de Pydantic y poder usar todos sus atributos/funciones
    """TODO: declara y valida los metadatos del bundle."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(ARTIFACT_SCHEMA_VERSION)
    model_version: str = Field(min_length=1)
    preprocessing_version: str
    feature_names: tuple[str, ...]
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)

    @field_validator("schema") # cuando se cree un objeto de esta clase, se activa @field_validator
    @classmethod
    def validate_schema_version(cls, value:str) -> str:
        """
        Impide crear el manifest si la versión es inválida
        """
        if value != ARTIFACT_SCHEMA_VERSION:
            raise ValueError(f"Ha fallado la creación del manifest debido a que no cumple la versión {ARTIFACT_SCHEMA_VERSION}")
        print("Se va a crear el manifest con este schema_version")


@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest


def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """
    El objetivo de esta función es, en base al estimator y model_version que recibe,
    devolver un ArtifactManifest. 
    Las variables mayúsculas son constantes y globales a todo el script (las puedo utilizar dentro de las clases)
    """

    return ArtifactManifest(
        schema_version = ARTIFACT_SCHEMA_VERSION,
        model_version = model_version,
        preprocessing_version = PREPROCESSING_VERSION,
        feature_names = FEATURE_NAMES,
        output_labels = OUTPUT_LABELS,
        estimator_type = type(estimator).__name__ # para que no devuelva <object ...>
                                                  # __ es un atributo privado
    )

#json.loads ##########################
#claves con comillas simples, es un diccionario de python
#comillas dobles, es una representación en string de un json

def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,
    manifest: ArtifactManifest | None = None,
) -> ArtifactManifest:
    """TODO: escribe manifest.json y model.joblib de forma segura."""

    manifest_path: str = Path(bundle_path)

    if manifest is not None:

        with open(manifest_path / "manifest.json", "w") as m: #se normaliza la ruta para que de igual si es windows o linux
            json.dump(manifest, m, indent=4, ensure_ascii=False)
            




def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """TODO: valida el manifiesto antes de cargar el estimador."""

    raise NotImplementedError("Implementa load_model_bundle().")


def infer_wine_quality(
    bundle: LoadedModelBundle,
    request: WineQualityRequest,
) -> WineQualityPrediction:
    """TODO: preprocesa, invoca el estimador y valida la respuesta."""

    raise NotImplementedError("Implementa infer_wine_quality().")
