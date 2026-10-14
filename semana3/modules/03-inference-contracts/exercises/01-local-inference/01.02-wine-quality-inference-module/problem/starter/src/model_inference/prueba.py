import joblib

ruta_archivo = '/Users/santiago/Desktop/icai-muiaap-operacion-de-modelos/semana3/modules/03-inference-contracts/exercises/01-local-inference/01.02-wine-quality-inference-module/problem/starter/src/model_inference/wine_quality_classifier.joblib'

objeto_cargado = joblib.load(ruta_archivo)

print(objeto_cargado)

"""
Imprime esto:


{'estimator': RandomForestClassifier(class_weight='balanced_subsample', max_depth=8,
                       min_samples_leaf=2, n_estimators=200, random_state=42), 

'feature_names': ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 
                    'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 
                    'ph', 'sulphates', 'alcohol'], 

'model_version': 'wine-quality-rf-v1'}
"""


"""
En el manifest habría que añadir la:
    - versión de procesado
    - etiquetas de salida
    - más todo lo anterior


'feature_names' indica el orden de las variables (es importante, porque el mdoelo se entrenó)
"""