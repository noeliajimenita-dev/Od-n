from typing import Any

from src.supervisor.session_event import SessionEvent
from src.supervisor.session_event_service import SessionEventService


class SessionHistory:
    """Builds structured history summaries for Supervisor sessions."""

    def __init__(self, event_service: SessionEventService):
        if event_service is None:
            raise ValueError("Session event service is required")

        self.event_service = event_service

    def get_events(self, session_id: str) -> list[SessionEvent]:
        return self.event_service.get_session_events(session_id)

    def build_summary(self, session_id: str) -> dict[str, Any]:
        events = self.get_events(session_id)

        event_types: dict[str, int] = {}
        task_ids: list[str] = []

        for event in events:
            event_types[event.event_type] = (
                event_types.get(event.event_type, 0) + 1
            )

            if event.task_id and event.task_id not in task_ids:
                task_ids.append(event.task_id)

        return {
            "session_id": session_id,
            "total_events": len(events),
            "event_types": event_types,
            "task_ids": task_ids,
            "first_event": (
                events[0].timestamp.isoformat()
                if events
                else None
            ),
            "last_event": (
                events[-1].timestamp.isoformat()
                if events
                else None
            ),
        }

    def has_events(self, session_id: str) -> bool:
        return bool(self.get_events(session_id))
