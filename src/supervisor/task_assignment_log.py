from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class TaskAssignmentEvent:
    task_id: str
    worker_id: str
    event: str
    timestamp: str


class TaskAssignmentLog:
    """Keeps a history of Supervisor-to-worker assignment events."""

    def __init__(self):
        self._events: list[TaskAssignmentEvent] = []

    def record(
        self,
        task_id: str,
        worker_id: str,
        event: str,
    ) -> TaskAssignmentEvent:
        task_id = task_id.strip()
        worker_id = worker_id.strip()
        event = event.strip().lower()

        if not task_id:
            raise ValueError("Task ID cannot be empty")

        if not worker_id:
            raise ValueError("Worker ID cannot be empty")

        if not event:
            raise ValueError("Event cannot be empty")

        assignment_event = TaskAssignmentEvent(
            task_id=task_id,
            worker_id=worker_id,
            event=event,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        self._events.append(assignment_event)

        return assignment_event

    def list_events(self) -> list[TaskAssignmentEvent]:
        return list(self._events)

    def task_events(self, task_id: str) -> list[TaskAssignmentEvent]:
        task_id = task_id.strip()

        return [
            event
            for event in self._events
            if event.task_id == task_id
        ]

    def worker_events(self, worker_id: str) -> list[TaskAssignmentEvent]:
        worker_id = worker_id.strip()

        return [
            event
            for event in self._events
            if event.worker_id == worker_id
        ]

    def count(self) -> int:
        return len(self._events)

    def clear(self) -> None:
        self._events.clear()
