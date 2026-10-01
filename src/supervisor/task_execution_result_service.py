from typing import Any

from src.supervisor.task import Task
from src.supervisor.task_execution_result import TaskExecutionResult


class TaskExecutionResultService:
    """Manages structured results produced by task executions."""

    def __init__(self):
        self._results: dict[str, TaskExecutionResult] = {}

    def record_success(
        self,
        task: Task,
        output: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> TaskExecutionResult:
        self._validate_task(task)

        result = TaskExecutionResult(
            task_id=task.task_id,
            status="completed",
            output=output,
            metadata=dict(metadata or {}),
        )

        self._results[task.task_id] = result

        return result

    def record_failure(
        self,
        task: Task,
        error: str,
        metadata: dict[str, Any] | None = None,
    ) -> TaskExecutionResult:
        self._validate_task(task)

        if not error or not error.strip():
            raise ValueError("Error message cannot be empty")

        result = TaskExecutionResult(
            task_id=task.task_id,
            status="failed",
            error=error.strip(),
            metadata=dict(metadata or {}),
        )

        self._results[task.task_id] = result

        return result

    def get(self, task_id: str) -> TaskExecutionResult | None:
        return self._results.get(task_id.strip())

    def has_result(self, task_id: str) -> bool:
        return task_id.strip() in self._results

    def list_results(self) -> list[TaskExecutionResult]:
        return list(self._results.values())

    def count(self) -> int:
        return len(self._results)

    def summary(self) -> dict[str, int]:
        completed = 0
        failed = 0

        for result in self._results.values():
            if result.is_success:
                completed += 1
            elif result.is_failure:
                failed += 1

        return {
            "total": len(self._results),
            "completed": completed,
            "failed": failed,
        }

    def _validate_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")
