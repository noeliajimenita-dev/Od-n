from dataclasses import dataclass, field
from typing import Any

from src.supervisor.task import Task


@dataclass
class TaskStateSnapshot:
    """Serializable snapshot of a Supervisor task state."""

    task_id: str
    description: str
    bot_name: str | None
    priority: int
    status: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_task(cls, task: Task) -> "TaskStateSnapshot":
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        return cls(
            task_id=task.task_id,
            description=task.description,
            bot_name=task.bot_name,
            priority=task.priority,
            status=task.status,
            metadata=dict(task.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "bot_name": self.bot_name,
            "priority": self.priority,
            "status": self.status,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "TaskStateSnapshot":
        if not isinstance(data, dict):
            raise TypeError("Expected a dictionary")

        task_id = data.get("task_id")

        if not isinstance(task_id, str) or not task_id.strip():
            raise ValueError("Task ID cannot be empty")

        return cls(
            task_id=task_id.strip(),
            description=str(data.get("description", "")),
            bot_name=data.get("bot_name"),
            priority=int(data.get("priority", 0)),
            status=str(data.get("status", "pending")),
            metadata=dict(data.get("metadata", {})),
        )

    def to_task(self) -> Task:
        return Task(
            task_id=self.task_id,
            description=self.description,
            bot_name=self.bot_name,
            priority=self.priority,
            status=self.status,
            metadata=dict(self.metadata),
  )
