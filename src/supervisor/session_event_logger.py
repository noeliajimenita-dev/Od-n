from typing import Any

from src.supervisor.session_event import SessionEvent
from src.supervisor.session_event_service import SessionEventService


class SessionEventLogger:
    """Logs important lifecycle events for Supervisor sessions."""

    def __init__(self, event_service: SessionEventService):
        if event_service is None:
            raise ValueError("Session event service is required")

        self.event_service = event_service

    def session_created(
        self,
        session_id: str,
        details: dict[str, Any] | None = None,
    ) -> SessionEvent:
        return self.event_service.record(
            session_id=session_id,
            event_type="session_created",
            details=details,
        )

    def session_paused(
        self,
        session_id: str,
        details: dict[str, Any] | None = None,
    ) -> SessionEvent:
        return self.event_service.record(
            session_id=session_id,
            event_type="session_paused",
            details=details,
        )

    def session_resumed(
        self,
        session_id: str,
        details: dict[str, Any] | None = None,
    ) -> SessionEvent:
        return self.event_service.record(
            session_id=session_id,
            event_type="session_resumed",
            details=details,
        )

    def session_closed(
        self,
        session_id: str,
        details: dict[str, Any] | None = None,
    ) -> SessionEvent:
        return self.event_service.record(
            session_id=session_id,
            event_type="session_closed",
            details=details,
        )

    def task_event(
        self,
        session_id: str,
        task_id: str,
        event_type: str,
        details: dict[str, Any] | None = None,
    ) -> SessionEvent:
        return self.event_service.record(
            session_id=session_id,
            event_type=event_type,
            task_id=task_id,
            details=details,
      )
