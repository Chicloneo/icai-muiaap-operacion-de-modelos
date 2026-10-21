"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Desde starter:
# uv run src/model_inference/predict_file.py --input assets/inference_samples.csv --output assets/predictions.csv 

# No dejes un archivo de salida parcial si alguna fila es inválida.

import argparse

import pandas as pd

from contracts import WineQualityRequest
from inference import DEFAULT_MODEL_PATH, infer_wine_quality, load_wine_quality_model
from preprocess import preprocess_wine_request


def read_wines(path):

    df = pd.read_csv(path, keep_default_na=False)
    df = df.drop("sample_id", axis=1)

    vinos_validados = []
    for index, row in df.iterrows():
        try:
            vino_valido = WineQualityRequest(**row.to_dict())
            vinos_validados.append(vino_valido)
        except Exception as e:
            raise ValueError(f"Error al validar el lote. Error en la muestra de vino \n {row}. Error: {e}")

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
    except ValueError as e: #porque hemos raiseado un ValueError
        print(e)
        return 2

    model = load_wine_quality_model(args.model)
    predicciones = []
    for vino in vinos_validados:
        fila_preprocesada = preprocess_wine_request(vino)
        prediccion = infer_wine_quality(model, fila_preprocesada)
        predicciones.append(prediccion.model_dump())

    df_predicciones = pd.DataFrame(predicciones)
    
    columna_IDs = pd.read_csv(args.input)["sample_id"]

    index=1
    for id in columna_IDs:
        if pd.isna(id):
            raise ValueError(f"Error. La muestra {index } no tiene ID")
        index+=1
        
    df = pd.concat([columna_IDs, df_predicciones], axis=1)
    df.to_csv(args.output, index=False)

    print(f"Se ha predicho la calidad de {len(predicciones)} vinos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())