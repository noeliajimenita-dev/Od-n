from src.supervisor.session_event import SessionEvent


class SessionEventRepository:
    """Stores and retrieves Supervisor session events."""

    def __init__(self):
        self._events: list[SessionEvent] = []

    def save(self, event: SessionEvent) -> SessionEvent:
        if not isinstance(event, SessionEvent):
            raise TypeError("Expected a SessionEvent")

        self._events.append(event)
        return event

    def get_all(self) -> list[SessionEvent]:
        return list(self._events)

    def get_by_session(self, session_id: str) -> list[SessionEvent]:
        if not session_id or not session_id.strip():
            return []

        normalized_id = session_id.strip()

        return [
            event
            for event in self._events
            if event.session_id == normalized_id
        ]

    def get_by_task(self, task_id: str) -> list[SessionEvent]:
        if not task_id or not task_id.strip():
            return []

        normalized_id = task_id.strip()

        return [
            event
            for event in self._events
            if event.task_id == normalized_id
        ]

    def get_by_type(self, event_type: str) -> list[SessionEvent]:
        if not event_type or not event_type.strip():
            return []

        normalized_type = event_type.strip()

        return [
            event
            for event in self._events
            if event.event_type == normalized_type
        ]

    def count(self) -> int:
        return len(self._events)

    def count_by_session(self, session_id: str) -> int:
        return len(self.get_by_session(session_id))

    def clear(self) -> None:
        self._events.clear()
