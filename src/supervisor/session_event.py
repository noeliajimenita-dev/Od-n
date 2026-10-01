from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class SessionEvent:
    """Represents an event recorded during a Supervisor session."""

    session_id: str
    event_type: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    task_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.session_id or not self.session_id.strip():
            raise ValueError("Session ID cannot be empty")

        if not self.event_type or not self.event_type.strip():
            raise ValueError("Event type cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "task_id": self.task_id,
            "details": dict(self.details),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SessionEvent":
        if not isinstance(data, dict):
            raise TypeError("Expected a dictionary")

        session_id = data.get("session_id")
        event_type = data.get("event_type")

        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("Session ID cannot be empty")

        if not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("Event type cannot be empty")

        timestamp_value = data.get("timestamp")

        if timestamp_value:
            timestamp = datetime.fromisoformat(timestamp_value)
        else:
            timestamp = datetime.now(timezone.utc)

        return cls(
            session_id=session_id.strip(),
            event_type=event_type.strip(),
            timestamp=timestamp,
            task_id=data.get("task_id"),
            details=dict(data.get("details", {})),
          )
