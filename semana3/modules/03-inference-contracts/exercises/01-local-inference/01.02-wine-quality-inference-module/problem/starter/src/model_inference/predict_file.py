"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Implementa el comando:
# python -m model_inference.predict_file --input <csv> --output <csv>
# No dejes un archivo de salida parcial si alguna fila es inválida.

import argparse

import pandas as pd

from .contracts import WineQualityRequest
from .inference import DEFAULT_MODEL_PATH, infer_wine_quality, load_wine_quality_model
from .preprocess import preprocess_wine_request


def read_wines(path):

    df = pd.read_csv(path, keep_default_na=False)
    df = df.drop("sample_id", axis=1)

    vinos_validados = []
    for index, row in df.iterrows():
        try:
            vino_valido = WineQualityRequest(**row.to_dict())
            vinos_validados.append(vino_valido)
        except:
            pass

    return vinos_validados



def main(argv=None):
    # Ya hecho: lee los argumentos --input, --output y --model.
    parser = argparse.ArgumentParser(description="Calidad de Vinos")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH)
    args = parser.parse_args(argv)  # noqa: F841


    try:
        vinos_validados = read_wines(args.input)
    except ValueError:
        return 2

    model = load_wine_quality_model(args.model)
    predicciones = []
    for vino in vinos_validados:
        fila_preprocesada = preprocess_wine_request(vino)
        prediccion = infer_wine_quality(model, fila_preprocesada)
        predicciones.append(prediccion.model_dump())

    df = pd.DataFrame(predicciones)
    df.to_csv(args.output, index=False)

    print(f"Se ha predicho la calidad de {len(predicciones)} vinos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())