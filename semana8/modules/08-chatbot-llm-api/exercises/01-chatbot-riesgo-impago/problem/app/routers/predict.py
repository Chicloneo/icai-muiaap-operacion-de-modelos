from fastapi import APIRouter

from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada
from app.services.modelo import predecir

router = APIRouter()

# TODO: POST /predict (entrada PrestamoEntrada, salida PrediccionSalida)

@router.post("/v1/predict")
def predict(prestamo: PrestamoEntrada) -> PrediccionSalida:

    return predecir(prestamo)