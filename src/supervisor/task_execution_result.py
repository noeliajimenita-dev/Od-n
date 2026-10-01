from dataclasses import dataclass, field
from typing import Any


@dataclass
class TaskExecutionResult:
    """Structured result returned after executing a Supervisor task."""

    task_id: str
    status: str
    output: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        return self.status == "completed"

    @property
    def is_failure(self) -> bool:
        return self.status == "failed"

    def add_metadata(self, key: str, value: Any) -> None:
        key = key.strip()

        if not key:
            raise ValueError("Metadata key cannot be empty")

        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "metadata": dict(self.metadata),
        }
