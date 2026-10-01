from datetime import datetime
from typing import Any

from src.supervisor.session_event import SessionEvent
from src.supervisor.session_event_filter import SessionEventFilter
from src.supervisor.session_history import SessionHistory


class SessionHistoryService:
    """Provides controlled queries over Supervisor session history."""

    def __init__(
        self,
        history: SessionHistory,
        event_filter: SessionEventFilter | None = None,
    ):
        if history is None:
            raise ValueError("Session history is required")

        self.history = history
        self.event_filter = event_filter or SessionEventFilter()

    def get_session_events(self, session_id: str) -> list[SessionEvent]:
        return self.history.get_events(session_id)

    def get_event_summary(self, session_id: str) -> dict[str, Any]:
        return self.history.build_summary(session_id)

    def get_events_by_type(
        self,
        session_id: str,
        event_type: str,
    ) -> list[SessionEvent]:
        events = self.get_session_events(session_id)
        return self.event_filter.by_type(events, event_type)

    def get_events_by_task(
        self,
        session_id: str,
        task_id: str,
    ) -> list[SessionEvent]:
        events = self.get_session_events(session_id)
        return self.event_filter.by_task(events, task_id)

    def get_events_by_time_range(
        self,
        session_id: str,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[SessionEvent]:
        events = self.get_session_events(session_id)

        return self.event_filter.by_time_range(
            events,
            start=start,
            end=end,
        )

    def get_latest_events(
        self,
        session_id: str,
        limit: int = 10,
    ) -> list[SessionEvent]:
        if limit <= 0:
            return []

        events = self.get_session_events(session_id)
        ordered = self.event_filter.sort_by_time(
            events,
            reverse=True,
        )

        return ordered[:limit]

    def has_history(self, session_id: str) -> bool:
        return self.history.has_events(session_id)
