"""
Gestor del Audit Log de THE ODIN PROJECT.
"""

from .event import AuditEvent


class AuditLogger:
    """Administra los eventos de auditoría en memoria."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> AuditEvent:
        """Registra un evento válido."""
        if not event.is_valid():
            errors = ", ".join(event.validate())
            raise ValueError(
                f"Evento de auditoría inválido: {errors}"
            )

        if any(
            existing.event_id == event.event_id
            for existing in self._events
        ):
            raise ValueError(
                f"El evento ya existe: {event.event_id}"
            )

        self._events.append(event)
        return event

    def get_event(self, event_id: str) -> AuditEvent | None:
        """Obtiene un evento por su identificador."""
        for event in self._events:
            if event.event_id == event_id:
                return event

        return None

    def get_all_events(self) -> list[AuditEvent]:
        """Devuelve una copia de todos los eventos."""
        return list(self._events)

    def count(self) -> int:
        """Devuelve la cantidad de eventos registrados."""
        return len(self._events)

    def clear(self) -> None:
        """
        Vacía el registro en memoria.

        Esta función existe únicamente para pruebas locales.
        La persistencia real y las protecciones contra eliminación
        se implementarán en módulos posteriores.
        """
        self._events.clear()
