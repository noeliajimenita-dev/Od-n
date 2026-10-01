from typing import Any

from src.supervisor.session_event import SessionEvent
from src.supervisor.session_history_service import SessionHistoryService


class SessionHistoryExporter:
    """Exports Supervisor session history into serializable structures."""

    def __init__(self, history_service: SessionHistoryService):
        if history_service is None:
            raise ValueError("Session history service is required")

        self.history_service = history_service

    def export_events(self, session_id: str) -> list[dict[str, Any]]:
        events = self.history_service.get_session_events(session_id)

        return [
            event.to_dict()
            for event in events
        ]

    def export_summary(self, session_id: str) -> dict[str, Any]:
        return self.history_service.get_event_summary(session_id)

    def export_latest(
        self,
        session_id: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        events = self.history_service.get_latest_events(
            session_id,
            limit=limit,
        )

        return [
            event.to_dict()
            for event in events
        ]

    def export_task_history(
        self,
        session_id: str,
        task_id: str,
    ) -> list[dict[str, Any]]:
        events = self.history_service.get_events_by_task(
            session_id,
            task_id,
        )

        return [
            event.to_dict()
            for event in events
        ]
