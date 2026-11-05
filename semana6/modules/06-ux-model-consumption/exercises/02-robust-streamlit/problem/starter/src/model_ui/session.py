"""Estado de sesión de Streamlit aislado para poder probarlo sin Streamlit."""

from __future__ import annotations

from collections.abc import MutableMapping

LAST_STATE_KEY = "last_state"
TELEMETRY_KEY = "telemetry"
LAST_VALUES_KEY = "last_values"


def initialize_session_state(
    session_state: MutableMapping[str, object],
) -> None:
    session_state = {}


def clear_last_state(session_state: MutableMapping[str, object]) -> None:
    """TODO: vuelve a idle sin perder la telemetría acumulada."""

    ultimo_elem = list(session_state)[-1]
    session_state.pop(ultimo_elem)
