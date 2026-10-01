from dataclasses import dataclass, field
from typing import Any


@dataclass
class SessionState:
    """Represents the current state of a Supervisor session."""

    session_id: str
    status: str = "active"
    task_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_task(self, task_id: str) -> None:
        if not task_id or not task_id.strip():
            raise ValueError("Task ID cannot be empty")

        normalized_id = task_id.strip()

        if normalized_id not in self.task_ids:
            self.task_ids.append(normalized_id)

    def remove_task(self, task_id: str) -> bool:
        if not task_id or not task_id.strip():
            return False

        normalized_id = task_id.strip()

        if normalized_id not in self.task_ids:
            return False

        self.task_ids.remove(normalized_id)
        return True

    def activate(self) -> None:
        self.status = "active"

    def pause(self) -> None:
        self.status = "paused"

    def close(self) -> None:
        self.status = "closed"

    def set_metadata(self, key: str, value: Any) -> None:
        if not key or not key.strip():
            raise ValueError("Metadata key cannot be empty")

        self.metadata[key.strip()] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "status": self.status,
            "task_ids": list(self.task_ids),
            "metadata": dict(self.metadata),
      }
