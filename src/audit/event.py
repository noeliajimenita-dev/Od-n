"""
Modelo de eventos de auditoría de THE ODIN PROJECT.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    """Devuelve la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class AuditEvent:
    """Representa un evento registrado en el sistema de auditoría."""

    event_id: str
    actor: str
    action: str
    reason: str
    result: str

    timestamp: datetime = field(default_factory=utc_now)

    task_id: str | None = None
    version: str | None = None
    authorization_id: str | None = None

    tokens_used: int = 0
    files_changed: list[str] = field(default_factory=list)

    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        """Comprueba que los datos básicos del evento sean válidos."""
        errors = []

        if not self.event_id:
            errors.append("event_id no puede estar vacío.")

        if not self.actor:
            errors.append("actor no puede estar vacío.")

        if not self.action:
            errors.append("action no puede estar vacío.")

        if not self.reason:
            errors.append("reason no puede estar vacío.")

        if not self.result:
            errors.append("result no puede estar vacío.")

        if self.tokens_used < 0:
            errors.append("tokens_used no puede ser negativo.")

        return errors

    def is_valid(self) -> bool:
        """Indica si el evento contiene datos válidos."""
        return len(self.validate()) == 0

    def to_dict(self) -> dict[str, Any]:
        """Convierte el evento en un diccionario serializable."""
        return {
            "event_id": self.event_id,
            "actor": self.actor,
            "action": self.action,
            "reason": self.reason,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
            "task_id": self.task_id,
            "version": self.version,
            "authorization_id": self.authorization_id,
            "tokens_used": self.tokens_used,
            "files_changed": list(self.files_changed),
            "error": self.error,
            "metadata": dict(self.metadata),
      }
