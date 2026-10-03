from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable


@dataclass(frozen=True)
class AIGateDecision:
    use_ai: bool
    reason: str
    local_action: str


class OdinAIUsageGate:
    """
    Decide cuándo ODIN debe utilizar Gemini.

    Objetivo:
    - Mantener al bot trabajando aunque Gemini no sea necesario.
    - Reservar IA para tareas que realmente la necesitan.
    - Evitar consumir rápidamente la cuota diaria.
    - Respetar límites RPM y RPD configurables.

    Los valores por defecto están pensados para el proyecto mostrado
    actualmente en Google AI Studio:
        RPM = 5
        RPD = 20
    """

    AI_KEYWORDS = {
        "analyze",
        "analysis",
        "analizar",
        "analisis",
        "analizar",
        "generate",
        "generar",
        "write",
        "escribir",
        "proposal",
        "propuesta",
        "program",
        "programar",
        "code",
        "codigo",
        "code_review",
        "review",
        "reason",
        "razonar",
        "strategy",
        "estrategia",
        "summarize",
        "resumir",
        "classify",
        "clasificar",
        "extract",
        "extraer",
        "creative",
        "creativo",
        "translate",
        "traducir",
        "decision",
        "decidir",
    }

    LOCAL_KEYWORDS = {
        "search",
        "buscar",
        "filter",
        "filtrar",
        "sort",
        "ordenar",
        "log",
        "registro",
        "status",
        "estado",
        "health",
        "salud",
        "backup",
        "respaldo",
        "schedule",
        "horario",
        "scheduler",
        "wait",
        "esperar",
        "queue",
        "cola",
        "deduplicate",
        "duplicados",
        "duplicate",
        "duplicado",
        "count",
        "contar",
        "validate",
        "validar",
        "cache",
        "cached",
        "quota",
        "cuota",
    }

    def __init__(
        self,
        max_requests_per_minute: int = 5,
        max_requests_per_day: int = 20,
        minimum_interval_seconds: float | None = None,
    ) -> None:
        if max_requests_per_minute <= 0:
            raise ValueError("max_requests_per_minute must be greater than zero")

        if max_requests_per_day <= 0:
            raise ValueError("max_requests_per_day must be greater than zero")

        self.max_requests_per_minute = max_requests_per_minute
        self.max_requests_per_day = max_requests_per_day

        self.minimum_interval_seconds = (
            minimum_interval_seconds
            if minimum_interval_seconds is not None
            else 60.0 / max_requests_per_minute
        )

        self._request_times: list[datetime] = []
        self._last_request_at: datetime | None = None
        self._daily_request_count = 0
        self._daily_date = datetime.now().date()

    # ------------------------------------------------------------------
    # PUBLIC DECISION API
    # ------------------------------------------------------------------

    def decide(
        self,
        task_type: str,
        description: str = "",
        complexity: str = "auto",
    ) -> AIGateDecision:
        """
        Decide si la tarea debe ir a Gemini o resolverse localmente.
        """

        self._reset_daily_counter_if_needed()

        task = f"{task_type} {description}".lower().strip()

        if complexity.lower() in {"low", "simple", "local"}:
            return AIGateDecision(
                use_ai=False,
                reason="Tarea simple/local.",
                local_action="Procesar localmente.",
            )

        if complexity.lower() in {"high", "complex", "ai"}:
            if not self.can_use_ai():
                return AIGateDecision(
                    use_ai=False,
                    reason="Cuota o intervalo de Gemini no disponible.",
                    local_action="Procesar localmente o poner en cola.",
                )

            return AIGateDecision(
                use_ai=True,
                reason="La tarea requiere razonamiento o generación.",
                local_action="",
            )

        tokens = self._tokenize(task)

        ai_matches = tokens.intersection(self.AI_KEYWORDS)
        local_matches = tokens.intersection(self.LOCAL_KEYWORDS)

        if local_matches and not ai_matches:
            return AIGateDecision(
                use_ai=False,
                reason="La tarea puede resolverse sin IA.",
                local_action="Procesar localmente.",
            )

        if ai_matches:
            if not self.can_use_ai():
                return AIGateDecision(
                    use_ai=False,
                    reason="Gemini alcanzó su límite operativo local.",
                    local_action="Procesar localmente o poner en cola.",
                )

            return AIGateDecision(
                use_ai=True,
                reason="La tarea necesita capacidades de IA.",
                local_action="",
            )

        # Por seguridad, tareas desconocidas no consumen Gemini
        # automáticamente.
        return AIGateDecision(
            use_ai=False,
            reason="Tipo de tarea no identificado como necesidad de IA.",
            local_action="Procesar localmente o clasificar antes de llamar a Gemini.",
        )

    # ------------------------------------------------------------------
    # QUOTA CONTROL
    # ------------------------------------------------------------------

    def can_use_ai(self, now: datetime | None = None) -> bool:
        """
        Comprueba si todavía podemos realizar una solicitud a Gemini.
        """

        now = now or datetime.now()

        self._reset_daily_counter_if_needed(now)
        self._cleanup_minute_window(now)

        if self._daily_request_count >= self.max_requests_per_day:
            return False

        if len(self._request_times) >= self.max_requests_per_minute:
            return False

        if self._last_request_at is not None:
            elapsed = (now - self._last_request_at).total_seconds()

            if elapsed < self.minimum_interval_seconds:
                return False

        return True

    def register_ai_request(self, now: datetime | None = None) -> None:
        """
        Registra una llamada real realizada a Gemini.

        Debe ejecutarse después de que ODIN decida utilizar Gemini.
        """

        now = now or datetime.now()

        self._reset_daily_counter_if_needed(now)
        self._cleanup_minute_window(now)

        if not self.can_use_ai(now):
            raise RuntimeError(
                "Gemini request blocked by ODIN AI usage limits."
            )

        self._request_times.append(now)
        self._last_request_at = now
        self._daily_request_count += 1

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def status(self, now: datetime | None = None) -> dict:
        now = now or datetime.now()

        self._reset_daily_counter_if_needed(now)
        self._cleanup_minute_window(now)

        return {
            "daily_requests_used": self._daily_request_count,
            "daily_requests_limit": self.max_requests_per_day,
            "daily_requests_remaining": max(
                0,
                self.max_requests_per_day - self._daily_request_count,
            ),
            "requests_last_minute": len(self._request_times),
            "requests_per_minute_limit": self.max_requests_per_minute,
            "can_use_ai": self.can_use_ai(now),
            "last_request_at": (
                self._last_request_at.isoformat()
                if self._last_request_at
                else None
            ),
        }

    # ------------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------------

    def _reset_daily_counter_if_needed(
        self,
        now: datetime | None = None,
    ) -> None:
        now = now or datetime.now()

        if now.date() != self._daily_date:
            self._daily_date = now.date()
            self._daily_request_count = 0
            self._request_times.clear()
            self._last_request_at = None

    def _cleanup_minute_window(self, now: datetime) -> None:
        cutoff = now - timedelta(minutes=1)

        self._request_times = [
            request_time
            for request_time in self._request_times
            if request_time > cutoff
        ]

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        normalized = (
            text.lower()
            .replace("-", " ")
            .replace("_", " ")
            .replace(",", " ")
            .replace(".", " ")
            .replace(":", " ")
            .replace(";", " ")
        )

        return {
            token
            for token in normalized.split()
            if token
        }


__all__ = [
    "AIGateDecision",
    "OdinAIUsageGate",
  ]
        
