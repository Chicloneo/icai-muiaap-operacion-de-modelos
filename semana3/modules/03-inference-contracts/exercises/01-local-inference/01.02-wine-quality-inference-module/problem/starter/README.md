# Starter — Módulo local de inferencia de vino

## ¿Qué es esto?
Modulo de predicción de calidad de vino. debe ejecutarse 
```bash
python src/model_inference/predict_file.py --input assets/inference_samples.csv --output assets/predictions.csv 
```
`inference_samples.csv` es un dataset de prueba. `predictions.csv` es un archivo con la predicción de la calidad del vino para cada muestra. Opcionalmente, puede añadirse `--model ruta/al/modelo.joblib` . Pero funciona con uno por defecto (no está en este repo).

`inference_samples_error.csv` debe fallar (intencionadamente) la validación de la muestra `red-002`.

### Pipeline

- `contracts.py`: contrato de datos de entrada y salida con Pydantic

- `preprocess.py`: preprocesado de los datos y su preparación para darlo como vector al modelo

- `inference.py`: inferencia del modelo (de Machine Learning).

- `predict_file.py`: funciona como un CLI . Es el orquestador de toda la práctica.

## Comentarios del profesor

Este es el único proyecto de código que recibe el alumnado. Implementad los
`TODO` siguiendo el orden del `../readme.md` y haced pasar las pruebas sin mirar
la solución del profesorado.

El profesor colocará `wine_quality_classifier.joblib` dentro de `models/` antes
del taller. El modelo ya está entrenado: no hay que modificarlo ni reentrenarlo.
