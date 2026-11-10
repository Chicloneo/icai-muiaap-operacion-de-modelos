"""Starter del cliente HTTP. Completa los TODO sin modificar la API."""

from __future__ import annotations

from typing import Any

# El TODO de la práctica usará este cliente para realizar la petición HTTP.
import requests  # noqa: F401


class PredictionClientError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


def request_prediction(
    payload: dict[str, Any],
    *,
    base_url: str = "http://127.0.0.1:8000",
    timeout: float = 5.0,
    session: Any | None = None,
) -> dict[str, Any]:
    """Envía una predicción y devuelve un objeto JSON de respuesta."""
    try:
        
        # TODO 3: selecciona `session` o `requests` y envía POST con `json=`,
        # `Accept` y `timeout`. Comprueba los argumentos con test_client.py.
        response = session.post(url=f"{base_url}/v1/predictions",
                json=payload,
                headers={"Accept": "application/json"},
                timeout=timeout)
    except requests.Timeout as error:
        # TODO 5: traduce Timeout y ConnectionError a PredictionClientError.
        raise PredictionClientError("Reintentar. Límite de tiempo alcanzado.") from error
    except requests.ConnectionError as error:
        # TODO 6: convierte la respuesta con `.json()` y exige un diccionario.
        raise PredictionClientError("Revisar la url. Error de conexión. No se pudo conectar con la API") from error

    try:
        
        # TODO 4: llama a `raise_for_status()` y conserva el status de HTTPError.
        response.raise_for_status()
        #Si hay un error HTTP, raise_for_status() lanza requests.HTTPError y salta esas líneas,
        #así que hay que capturar ese error.

    except requests.HTTPError as error:
        status_code = response.status_code
        raise PredictionClientError("Datos introducidos en formato inválido", status_code=status_code) from error

    if not isinstance(response.json(), dict):
        raise PredictionClientError("La respuesta no es un objeto json")
    
    return response.json()

class RecordingSession:
    def __init__(self, response=None, exception=None):
        self.response = response or FakeResponse()
        self.exception = exception
        self.call = None

    def post(self, url, **kwargs):
        self.call = (url, kwargs)
        if self.exception:
            raise self.exception
        return self.response
