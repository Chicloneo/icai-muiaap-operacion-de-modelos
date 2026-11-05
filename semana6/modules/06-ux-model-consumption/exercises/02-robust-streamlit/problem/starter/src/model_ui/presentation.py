"""TODOs de la vista UX: copy de salida y traducción de errores."""

from __future__ import annotations

from model_ui.contracts import PredictionPayload, PredictionView, UserFacingError
from model_ui.policies import (
    DEFAULT_CONFIDENCE_POLICY,
    DEFAULT_LATENCY_POLICY,
    ConfidencePolicy,
    LatencyPolicy,
    classify_confidence,
    classify_latency
)

QUALITY_LABELS = {
    "needs_review": "Requiere revisión",
    "acceptable": "Resultado aceptable",
    "excellent": "Resultado excelente",
}

CONFIDENCE_COPY = {
    "low": (
        "Confianza baja",
        "El resultado es orientativo y requiere revisión; "
        "la confianza no es una garantía.",
    ),
    "medium": (
        "Confianza intermedia",
        "Usa el resultado como señal orientativa y revisa su contexto antes de actuar.",
    ),
    "high": (
        "Confianza alta",
        "La confianza es alta para este modelo, pero no garantiza "
        "que la decisión sea correcta.",
    ),
}

LATENCY_COPY = {
    "within_target": (
        "Dentro del objetivo",
        "La respuesta quedó dentro del objetivo de la demo.",
    ),
    "above_target": (
        "Por encima del objetivo",
        "La respuesta llegó, pero la latencia supera el objetivo técnico de la demo.",
    ),
}


def build_prediction_view(
    prediction: PredictionPayload,
    latency_ms: float,
    *,
    confidence_policy: ConfidencePolicy = DEFAULT_CONFIDENCE_POLICY,
    latency_policy: LatencyPolicy = DEFAULT_LATENCY_POLICY,
) -> PredictionView:
    """TODO: construye la vista con etiquetas, confianza, latencia y versiones."""

    return PredictionView(
    quality_band=prediction.quality_band,
    quality_label=QUALITY_LABELS[prediction.quality_band],
    confidence=prediction.confidence,
    confidence_level=classify_confidence(confidence = prediction.confidence, policy = confidence_policy),
    confidence_label=CONFIDENCE_COPY[classify_confidence(prediction.confidence,confidence_policy)][0],
    confidence_message=CONFIDENCE_COPY[classify_confidence(prediction.confidence,confidence_policy)][1],
    latency_ms=latency_ms,
    latency_status=classify_latency(latency_ms=latency_ms, policy=latency_policy),
    latency_label=LATENCY_COPY[classify_latency(latency_ms, latency_policy)][0],
    latency_message=LATENCY_COPY[classify_latency(latency_ms, latency_policy)][1],
    model_version=prediction.model_version,
    preprocessing_version=prediction.preprocessing_version
    )


def to_user_facing_error(error: Exception, request_id: str) -> UserFacingError:
    """TODO: asigna código estable, mensaje accionable y recuperación."""

    return UserFacingError(
    code=error.errno,
    title="Error",
    message=str(error),
    recovery="Vuelve a intentar",
    request_id=request_id
    )