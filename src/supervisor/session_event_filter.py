from datetime import datetime

from src.supervisor.session_event import SessionEvent


class SessionEventFilter:
    """Filters session events using common history criteria."""

    def by_type(
        self,
        events: list[SessionEvent],
        event_type: str,
    ) -> list[SessionEvent]:
        if not event_type or not event_type.strip():
            return []

        normalized_type = event_type.strip()

        return [
            event
            for event in events
            if event.event_type == normalized_type
        ]

    def by_task(
        self,
        events: list[SessionEvent],
        task_id: str,
    ) -> list[SessionEvent]:
        if not task_id or not task_id.strip():
            return []

        normalized_task_id = task_id.strip()

        return [
            event
            for event in events
            if event.task_id == normalized_task_id
        ]

    def by_time_range(
        self,
        events: list[SessionEvent],
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[SessionEvent]:
        filtered = []

        for event in events:
            if start is not None and event.timestamp < start:
                continue

            if end is not None and event.timestamp > end:
                continue

            filtered.append(event)

        return filtered

    def sort_by_time(
        self,
        events: list[SessionEvent],
        reverse: bool = False,
    ) -> list[SessionEvent]:
        return sorted(
            events,
            key=lambda event: event.timestamp,
            reverse=reverse,
        )
