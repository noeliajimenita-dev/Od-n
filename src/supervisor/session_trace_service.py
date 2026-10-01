from typing import Any

from src.supervisor.session_event import SessionEvent
from src.supervisor.session_event_service import SessionEventService
from src.supervisor.session_history_service import SessionHistoryService


class SessionTraceService:
    """Central service for Supervisor session traceability."""

    def __init__(
        self,
        event_service: SessionEventService,
        history_service: SessionHistoryService,
    ):
        if event_service is None:
            raise ValueError("Session event service is required")

        if history_service is None:
            raise ValueError("Session history service is required")

        self.event_service = event_service
        self.history_service = history_service

    def record(
        self,
        session_id: str,
        event_type: str,
        task_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> SessionEvent:
        return self.event_service.record(
            session_id=session_id,
            event_type=event_type,
            task_id=task_id,
            details=details,
        )

    def get_trace(self, session_id: str) -> list[SessionEvent]:
        return self.history_service.get_session_events(session_id)

    def get_summary(self, session_id: str) -> dict[str, Any]:
        return self.history_service.get_event_summary(session_id)

    def get_task_trace(
        self,
        session_id: str,
        task_id: str,
    ) -> list[SessionEvent]:
        return self.history_service.get_events_by_task(
            session_id,
            task_id,
        )

    def get_latest(
        self,
        session_id: str,
        limit: int = 10,
    ) -> list[SessionEvent]:
        return self.history_service.get_latest_events(
            session_id,
            limit=limit,
        )

    def has_trace(self, session_id: str) -> bool:
        return self.history_service.has_history(session_id)
