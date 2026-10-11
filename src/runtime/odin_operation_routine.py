
"""Rutina operativa de ODIN: pausas, límites y validación humana."""

from dataclasses import dataclass
from enum import Enum
import random
import threading
import time
from typing import Callable


class RoutineState(str, Enum):
    READY = "ready"
    WAITING = "waiting"
    PAUSED_FOR_HUMAN = "paused_for_human"
    STOPPED = "stopped"


@dataclass(frozen=True)
class RoutineConfig:
    min_action_interval_ms: int = 1500
    repetitive_step_interval_ms: int = 2150
    normal_pause_min_ms: int = 1500
    normal_pause_max_ms: int = 3000

    def __post_init__(self) -> None:
        if self.min_action_interval_ms < 0:
            raise ValueError("El intervalo mínimo no puede ser negativo")
        if self.repetitive_step_interval_ms < 0:
            raise ValueError("El intervalo repetitivo no puede ser negativo")
        if self.normal_pause_min_ms < 0:
            raise ValueError("La pausa mínima no puede ser negativa")
        if self.normal_pause_max_ms < self.normal_pause_min_ms:
            raise ValueError("La pausa máxima debe ser >= a la mínima")


class OdinOperationRoutine:
    """Regula el ritmo de tareas y exige aprobación ante verificaciones."""

    def __init__(
        self,
        config: RoutineConfig | None = None,
        notify_user: Callable[[str], None] | None = None,
    ) -> None:
        self.config = config or RoutineConfig()
        self.notify_user = notify_user or (lambda message: None)
        self._lock = threading.RLock()
        self._last_action_at: float | None = None
        self._state = RoutineState.READY
        self._human_approval = threading.Event()
        self._stop_event = threading.Event()

    @property
    def state(self) -> RoutineState:
        with self._lock:
            return self._state

    def wait_before_action(self, repetitive: bool = False) -> bool:
        """Espera el intervalo requerido sin llamar a proveedores de IA."""
        with self._lock:
            if self._state in (
                RoutineState.STOPPED,
                RoutineState.PAUSED_FOR_HUMAN,
            ):
                return False

            interval_ms = self.config.min_action_interval_ms
            if repetitive:
                interval_ms = max(
                    interval_ms,
                    self.config.repetitive_step_interval_ms,
                )

            if self._last_action_at is None:
                delay = 0.0
            else:
                elapsed_ms = (
                    time.monotonic() - self._last_action_at
                ) * 1000
                delay = max(0.0, (interval_ms - elapsed_ms) / 1000)

            self._state = (
                RoutineState.WAITING if delay > 0 else RoutineState.READY
            )

        if delay > 0 and self._stop_event.wait(delay):
            return False

        with self._lock:
            if self._state in (
                RoutineState.STOPPED,
                RoutineState.PAUSED_FOR_HUMAN,
            ):
                return False
            self._state = RoutineState.READY
            return True

    def mark_action_started(self) -> None:
        """Registrar el inicio de una acción previamente autorizada."""
        with self._lock:
            if self._state != RoutineState.READY:
                raise RuntimeError(
                    f"No se puede actuar en estado {self._state.value}"
                )
            self._last_action_at = time.monotonic()

    def wait_between_steps(self) -> bool:
        """Aplica una pausa configurable entre pasos de trabajo."""
        delay_ms = random.randint(
            self.config.normal_pause_min_ms,
            self.config.normal_pause_max_ms,
        )
        return not self._stop_event.wait(delay_ms / 1000)

    def pause_for_verification(self, reason: str) -> None:
        """Detenerse ante CAPTCHA, 2FA o validaciones de identidad."""
        with self._lock:
            if self._state == RoutineState.STOPPED:
                return
            self._state = RoutineState.PAUSED_FOR_HUMAN
            self._human_approval.clear()

        self.notify_user(
            "ODIN está en pausa y espera tu autorización. "
            f"Motivo: {reason}"
        )

    def approve_resume(self) -> bool:
        """Reanudar solo tras una aprobación explícita."""
        with self._lock:
            if self._state != RoutineState.PAUSED_FOR_HUMAN:
                return False
            self._state = RoutineState.READY
            self._human_approval.set()
            return True

    def wait_for_approval(self, timeout: float | None = None) -> bool:
        """Esperar aprobación; el timeout nunca reanuda por sí solo."""
        approved = self._human_approval.wait(timeout)
        if not approved:
            return False
        with self._lock:
            return self._state == RoutineState.READY

    def stop(self) -> None:
        """Detener la rutina y despertar las esperas pendientes."""
        with self._lock:
            self._state = RoutineState.STOPPED
            self._stop_event.set()
            self._human_approval.set()
