"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import joblib
from .contracts import WineQualityRequest, WineQualityPrediction
from .preprocess import preprocess_wine_request
from .artifact import load_model_bundle, MODEL_FILENAME, infer_wine_quality

from model_packaging.artifact import DEFAULT_BUNDLE_PATH


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """TODO: valida todas las filas y escribe el CSV solo al final."""

    df_id = pd.read_csv(input_path)
    df = df_id.drop('sample_id', axis=1)
    modelo = load_model_bundle(bundle_path)
    estimador = modelo.estimator

    predicciones = []
    for index, row in df.iterrows():
        request = WineQualityRequest(**row.to_dict())
        #features = preprocess_wine_request(request).as_vector()
        prediccion = infer_wine_quality(
            bundle = modelo,
            request= request
            )
        prediccion_dict = {
            "sample_id": df_id.loc[index, "sample_id"],
            **prediccion.model_dump(),
        }
        predicciones.append(prediccion_dict)

    df_final = pd.DataFrame(predicciones)
    df_final.to_csv(output_path, index=False) #solo escribimos al final

    return len(df_final)


def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(
        predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    )
