from __future__ import annotations

from typing import Any

from .odin_execution_engine import ExecutionResult


class SupervisorExecutionResultService:
    """Gestiona los resultados generados por la ejecución de tareas."""

    def __init__(self) -> None:
        self._results: dict[str, ExecutionResult] = {}

    def record(self, result: ExecutionResult) -> ExecutionResult:
        if result is None:
            raise ValueError("result cannot be None")

        if not result.task_id or not result.task_id.strip():
            raise ValueError("result task_id cannot be empty")

        self._results[result.task_id] = result
        return result

    def get(self, task_id: str) -> ExecutionResult | None:
        if not task_id or not task_id.strip():
            return None

        return self._results.get(task_id)

    def exists(self, task_id: str) -> bool:
        return self.get(task_id) is not None

    def is_successful(self, task_id: str) -> bool:
        result = self.get(task_id)

        if result is None:
            return False

        return result.status == "completed"

    def is_failed(self, task_id: str) -> bool:
        result = self.get(task_id)

        if result is None:
            return False

        return result.status == "error"

    def list_all(self) -> list[ExecutionResult]:
        return list(self._results.values())

    def list_successful(self) -> list[ExecutionResult]:
        return [
            result
            for result in self._results.values()
            if result.status == "completed"
        ]

    def list_failed(self) -> list[ExecutionResult]:
        return [
            result
            for result in self._results.values()
            if result.status == "error"
        ]

    def count(self) -> int:
        return len(self._results)

    def count_successful(self) -> int:
        return len(self.list_successful())

    def count_failed(self) -> int:
        return len(self.list_failed())

    def summary(self) -> dict[str, Any]:
        return {
            "total": self.count(),
            "successful": self.count_successful(),
            "failed": self.count_failed(),
            "task_ids": list(self._results.keys()),
        }

    def clear(self) -> None:
        self._results.clear()

    def remove(self, task_id: str) -> bool:
        if task_id not in self._results:
            return False

        del self._results[task_id]
        return True

    def __repr__(self) -> str:
        return (
            "SupervisorExecutionResultService("
            f"results={self.count()}"
            ")"
  )
