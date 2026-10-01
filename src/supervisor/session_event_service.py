from typing import Any

from src.supervisor.session_event import SessionEvent
from src.supervisor.session_event_repository import SessionEventRepository


class SessionEventService:
    """Provides controlled access to Supervisor session event logging."""

    def __init__(self, repository: SessionEventRepository):
        if repository is None:
            raise ValueError("Session event repository is required")

        self.repository = repository

    def record(
        self,
        session_id: str,
        event_type: str,
        task_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> SessionEvent:
        event = SessionEvent(
            session_id=session_id,
            event_type=event_type,
            task_id=task_id,
            details=dict(details or {}),
        )

        return self.repository.save(event)

    def record_event(self, event: SessionEvent) -> SessionEvent:
        if not isinstance(event, SessionEvent):
            raise TypeError("Expected a SessionEvent")

        return self.repository.save(event)

    def get_session_events(self, session_id: str) -> list[SessionEvent]:
        return self.repository.get_by_session(session_id)

    def get_task_events(self, task_id: str) -> list[SessionEvent]:
        return self.repository.get_by_task(task_id)

    def get_events_by_type(self, event_type: str) -> list[SessionEvent]:
        return self.repository.get_by_type(event_type)

    def get_all_events(self) -> list[SessionEvent]:
        return self.repository.get_all()

    def count(self) -> int:
        return self.repository.count()

    def count_session_events(self, session_id: str) -> int:
        return self.repository.count_by_session(session_id)

    def clear(self) -> None:
        self.repository.clear()
