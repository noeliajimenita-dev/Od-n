from __future__ import annotations

from typing import Any

from src.supervisor.task import Task

from .odin_execution_engine import ExecutionResult
from .supervisor_execution_controller import (
    SupervisorExecutionController,
)
from .supervisor_execution_result_service import (
    SupervisorExecutionResultService,
)


class SupervisorExecutionOrchestrator:
    """Orquesta ejecución y almacenamiento de resultados."""

    def __init__(
        self,
        controller: SupervisorExecutionController,
        result_service: SupervisorExecutionResultService,
    ) -> None:
        if controller is None:
            raise ValueError("controller cannot be None")

        if result_service is None:
            raise ValueError(
                "result_service cannot be None"
            )

        self.controller = controller
        self.result_service = result_service

    def execute(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> ExecutionResult:
        result = self.controller.execute_task(
            task=task,
            worker_id=worker_id,
        )

        return self.result_service.record(result)

    def execute_with_ai(
        self,
        task: Task,
        prompt: str,
        model: str,
        worker_id: str | None = None,
        preferred_provider: str | None = None,
    ) -> ExecutionResult:
        result = self.controller.execute_task_with_ai(
            task=task,
            prompt=prompt,
            model=model,
            worker_id=worker_id,
            preferred_provider=preferred_provider,
        )

        return self.result_service.record(result)

    def assign(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> str:
        return self.controller.assign_task(
            task=task,
            worker_id=worker_id,
        )

    def get_result(
        self,
        task_id: str,
    ) -> ExecutionResult | None:
        return self.result_service.get(task_id)

    def is_successful(self, task_id: str) -> bool:
        return self.result_service.is_successful(
            task_id
        )

    def is_failed(self, task_id: str) -> bool:
        return self.result_service.is_failed(
            task_id
        )

    def summary(self) -> dict[str, Any]:
        return self.result_service.summary()

    def status(self) -> dict[str, Any]:
        return {
            "execution": self.controller.status(),
            "results": self.result_service.summary(),
        }

    def clear_results(self) -> None:
        self.result_service.clear()

    def __repr__(self) -> str:
        return (
            "SupervisorExecutionOrchestrator("
            f"results={self.result_service.count()}"
            ")"
        )
