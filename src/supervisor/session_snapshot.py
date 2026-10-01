from dataclasses import dataclass, field
from typing import Any

from src.supervisor.session_state import SessionState


@dataclass
class SessionSnapshot:
    """Serializable snapshot of a Supervisor session."""

    session_id: str
    status: str
    task_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_session(cls, session: SessionState) -> "SessionSnapshot":
        if not isinstance(session, SessionState):
            raise TypeError("Expected a SessionState instance")

        return cls(
            session_id=session.session_id,
            status=session.status,
            task_ids=list(session.task_ids),
            metadata=dict(session.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "status": self.status,
            "task_ids": list(self.task_ids),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "SessionSnapshot":
        if not isinstance(data, dict):
            raise TypeError("Expected a dictionary")

        session_id = data.get("session_id")

        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("Session ID cannot be empty")

        return cls(
            session_id=session_id.strip(),
            status=str(data.get("status", "active")),
            task_ids=list(data.get("task_ids", [])),
            metadata=dict(data.get("metadata", {})),
        )

    def to_session(self) -> SessionState:
        return SessionState(
            session_id=self.session_id,
            status=self.status,
            task_ids=list(self.task_ids),
            metadata=dict(self.metadata),
            )
