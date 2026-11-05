"""TODOs del controlador de estados independiente de Streamlit."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from time import perf_counter
from uuid import uuid4

from model_ui.contracts import UiState
from model_ui.errors import (
    ArtifactUnavailableError,
    BackendInferenceError,
    InferenceTimeoutError,
    InputContractError,
)
from model_ui.gateway import InferenceGateway
from model_ui.policies import DEFAULT_CONFIDENCE_POLICY, DEFAULT_LATENCY_POLICY
from model_ui.presentation import build_prediction_view, to_user_facing_error
from model_ui.telemetry import Telemetry

StateEmitter = Callable[[UiState], None]
Clock = Callable[[], float]
RequestIdFactory = Callable[[], str]


class PredictionController:
    """Orquesta loading, gateway, errores y telemetría."""

    def __init__(
        self,
        gateway: InferenceGateway,
        *,
        telemetry: Telemetry | None = None,
        clock: Clock = perf_counter,
        request_id_factory: RequestIdFactory | None = None,
    ) -> None:
        self.gateway = gateway
        self.telemetry = telemetry or Telemetry()
        self._clock = clock
        self._request_id_factory = request_id_factory or (lambda: uuid4().hex[:10])

    def submit(
        self,
        values: Mapping[str, object],
        *,
        emit: StateEmitter | None = None,
    ) -> UiState:
        """TODO: emite loading, mide, valida la salida y devuelve success/error."""

        request_id = self._request_id_factory()
        loading_state = UiState(phase="loading", request_id=request_id)
        if emit is not None:
            emit(loading_state)

        started_at = self._clock()
        try:
            prediction = self.gateway.predict(values)
            latency_ms = max(
                0.0, round((self._clock() - started_at) * 1000, 3)
            )
            view = build_prediction_view(
                prediction,
                latency_ms,
                confidence_policy=DEFAULT_CONFIDENCE_POLICY,
                latency_policy=DEFAULT_LATENCY_POLICY,
            )
        except (
            InputContractError,
            ArtifactUnavailableError,
            InferenceTimeoutError,
            BackendInferenceError,
        ) as error:
            latency_ms = max(
                0.0, round((self._clock() - started_at) * 1000, 3)
            )
            user_error = to_user_facing_error(error, request_id)
            self.telemetry.record_error(user_error.code, latency_ms)
            state = UiState(
                phase="error",
                request_id=request_id,
                error=user_error,
            )
        else:
            self.telemetry.record_success(
                latency_ms,
                model_version=view.model_version,
                preprocessing_version=view.preprocessing_version,
            )
            state = UiState(phase="success", request_id=request_id, view=view)

        if emit is not None:
            emit(state)
        return state
