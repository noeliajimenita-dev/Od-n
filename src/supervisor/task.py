from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    task_id: str
    description: str
    bot_name: str | None = None
    priority: int = 0
    status: str = "pending"
    metadata: dict[str, Any] = field(default_factory=dict)

    def assign(self, bot_name: str) -> None:
        self.bot_name = bot_name
        self.status = "assigned"

    def start(self) -> None:
        self.status = "running"

    def complete(self, result: Any = None) -> None:
        self.status = "completed"

        if result is not None:
            self.metadata["result"] = result

    def fail(self, error: str) -> None:
        self.status = "failed"
        self.metadata["error"] = error
