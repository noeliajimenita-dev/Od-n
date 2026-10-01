from typing import Any

from src.supervisor.task import Task
from src.supervisor.task_execution_controller import TaskExecutionController
from src.supervisor.task_execution_result import TaskExecutionResult
from src.supervisor.task_execution_result_service import (
    TaskExecutionResultService,
)


class TaskExecutionOrchestrator:
    """Provides a unified interface for executing Supervisor tasks."""

    def __init__(
        self,
        controller: TaskExecutionController,
        result_service: TaskExecutionResultService,
    ):
        if controller is None:
            raise ValueError("Task execution controller is required")

        if result_service is None:
            raise ValueError("Task execution result service is required")

        self.controller = controller
        self.result_service = result_service

    def execute(
        self,
        task: Task,
        handler: Any,
    ) -> TaskExecutionResult:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        try:
            output = self.controller.execute(
                task,
                handler,
            )

            return self.result_service.record_success(
                task,
                output=output,
            )

        except Exception as exc:
            return self.result_service.record_failure(
                task,
                error=str(exc),
            )

    def get_result(
        self,
        task_id: str,
    ) -> TaskExecutionResult | None:
        return self.result_service.get(task_id)

    def has_result(self, task_id: str) -> bool:
        return self.result_service.has_result(task_id)

    def summary(self) -> dict[str, int]:
        return self.result_service.summary()
