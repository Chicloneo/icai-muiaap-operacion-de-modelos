"""TODO: script CLI que encadena contratos, preprocesado e inferencia."""

# Desde starter:
# uv run python -m model_inference.predict_file --input assets/inference_samples.csv --output assets/predictions.csv 
# con -m le estamos diciendo a uv que model_inference es un módulo

# Mal: `uv run src/model_inference/predict_file.py` porque model_inference ya es un paquete con __init__, 
# así que lo puedo llamar

# No dejes un archivo de salida parcial si alguna fila es inválida.

import argparse

import pandas as pd

from .contracts import WineQualityRequest, SampleID
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

    #Validamos filas y falla si alguna no es válida
    try:
        vinos_validados = read_wines(args.input)
    except ValueError as e: #porque hemos raiseado un ValueError
        print(e)
        return 2

    #Cargamos el modelo y falla si no existe
    try:
        model = load_wine_quality_model(args.model)
    except ValueError as e:
        print(e)
        return 2

    #Predecimos la calidad del vino
    predicciones = []
    for vino in vinos_validados:
        fila_preprocesada = preprocess_wine_request(vino)
        prediccion = infer_wine_quality(model, fila_preprocesada)
        predicciones.append(prediccion.model_dump())

    df_predicciones = pd.DataFrame(predicciones)
    
    columna_IDs = pd.read_csv(args.input)["sample_id"]

    index = 1
    for id in columna_IDs:
        try:
            SampleID(sample_id=id)
        except Exception as e:
            print(f"Error en el id '{id}', en la fila {index}. Debe ser un string no vacío.")
            print(e)
            return 2
        index+=1

    #Añadimos la columna sample_id si todos son strings no vacíos
    df = pd.concat([columna_IDs, df_predicciones], axis=1)
    df.to_csv(args.output, index=False)

    print(f"Se ha predicho la calidad de {len(predicciones)} vinos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())