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

    esquema = PrestamoEntrada.model_json_schema() 

    return {
        "type": "function",
        "function": {
            "name": NOMBRE_TOOL,  
            "description": "Esta es una tool que calcula el riesgo de impago. \
                Para poder usarla necesitas los 6 datos del usuario", 
            "parameters": esquema, 
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


    historial = [{"role": "system", "content": SISTEMA}]
    for m in mensajes:
        historial.append({"role": m.role, "content": m.content})

    herramienta = None 

    for _ in range(MAX_VUELTAS):

        # ¿puedes contestar o quieres una tool?
        respuesta = llm.completar(historial, [definir_tool()])

        if not respuesta.get("tool_calls"):
            return ChatSalida(respuesta=respuesta["content"], herramienta=herramienta)

        historial.append(respuesta)

        # podría pedir varias tools
        for llamada in respuesta["tool_calls"]:
            nombre = llamada["function"]["name"]
            argumentos_json = llamada["function"]["arguments"]

            resultado = ejecutar_tool(nombre, argumentos_json)

            herramienta = HerramientaUsada(
                nombre=nombre,
                argumentos=leer_argumentos(argumentos_json),
                resultado=resultado,
            )

            historial.append({
                "role": "tool",
                "tool_call_id": llamada["id"],
                "content": json.dumps(resultado),
            })

    return ChatSalida(
        respuesta="No he podido completar la consulta con los datos disponibles.",
        herramienta=herramienta,
    )