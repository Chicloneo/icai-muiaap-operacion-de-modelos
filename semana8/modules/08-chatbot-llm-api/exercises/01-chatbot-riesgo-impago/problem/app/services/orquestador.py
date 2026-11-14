import json

from pydantic import ValidationError

from app.schemas.chat import ChatSalida, HerramientaUsada
from app.schemas.prestamo import PrestamoEntrada
from app.services.modelo import predecir

NOMBRE_TOOL = "calcular_riesgo_impago"
MAX_VUELTAS = 4

SISTEMA = (
    "Eres un asistente de riesgo de un banco. Cuando tengas todos los datos de una solicitud de "
    "prestamo, llama a la herramienta calcular_riesgo_impago. Si falta algun dato, pidelo. "
    "Nunca inventes valores. Responde en espanol y de forma breve."
)


def leer_argumentos(texto):
    """YA HECHO: convierte el texto JSON de la tool en dict ({} si no es JSON valido)."""
    try:
        datos = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    if isinstance(datos, dict):
        return datos
    return {}


# TODO: definir_tool() -> dict con la definicion de la tool, sacando "parameters" de PrestamoEntrada
def definir_tool() -> dict:
    esquema = PrestamoEntrada.model_json_schema()  # (1) el JSON Schema de PrestamoEntrada

    return {
        "type": "function",
        "function": {
            "name": NOMBRE_TOOL,          # (2) qué nombre
            "description": "descripción de la función",   # (3) qué le cuentas al LLM
            "parameters": esquema,    # (4) qué parte del esquema va aquí
        },
    }
# TODO: ejecutar_tool(nombre, argumentos_json) -> dict con "ok" True/False
#       (tool desconocida, JSON roto, datos invalidos o campos inventados -> ok False con el error)
def ejecutar_tool(nombre, argumentos_json) -> dict:

    if nombre != NOMBRE_TOOL:
        return {"ok":False,
                "error": "Tool desconocida. El nombre de la tool \
                    no corresponde con el nombre oficial"}

    try:
        prestamo = PrestamoEntrada(**leer_argumentos(argumentos_json))
        prediccion = predecir(prestamo)
        return {"ok":True,
                "probabilidad_impago": prediccion.probabilidad_impago,
                "decision": prediccion.decision}
    except ValidationError as e:
        return {"ok":False,
                "error": f"Fallo en la validación de los datos. \
                    Posibles razones: json roto, datos inválidos, \
                        campos inventados, ... \
                            \n Error: {e}"}
    
# TODO: responder(mensajes, llm) -> ChatSalida, con el bucle LLM -> tool -> LLM (maximo MAX_VUELTAS)
def responder(mensajes, llm) -> ChatSalida:
    
    for i in range(MAX_VUELTAS):

        tool = ejecutar_tool(nombre=NOMBRE_TOOL, argumentos_json=mensajes)
        llm.completar(mensajes, herramientas=HerramientaUsada)

    return ChatSalida(
        respuesta="",
        herramienta=HerramientaUsada,
    )
