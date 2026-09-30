from dataclasses import dataclass
from typing import Any


@dataclass
class SupervisorResult:
    task_id: str
    status: str
    result: Any = None
    error: str | None = None


class Supervisor:
    def __init__(self, dispatcher=None, executor=None, reporter=None):
        self.dispatcher = dispatcher
        self.executor = executor
        self.reporter = reporter
        self.active_tasks: dict[str, Any] = {}

    def register_task(self, task_id: str, task: Any) -> None:
        self.active_tasks[task_id] = task

    def execute(self, task_id: str) -> SupervisorResult:
        if task_id not in self.active_tasks:
            return SupervisorResult(
                task_id=task_id,
                status="error",
                error="Task not found",
            )

        task = self.active_tasks[task_id]

        try:
            if self.dispatcher is not None:
                task = self.dispatcher.dispatch(task)

            if self.executor is not None:
                result = self.executor.execute(task)
            else:
                result = task

            return SupervisorResult(
                task_id=task_id,
                status="completed",
                result=result,
            )

        except Exception as exc:
            return SupervisorResult(
                task_id=task_id,
                status="error",
                error=str(exc),
            )

    def get_status(self) -> dict[str, Any]:
        return {
            "active_tasks": len(self.active_tasks),
            "task_ids": list(self.active_tasks.keys()),
          }
