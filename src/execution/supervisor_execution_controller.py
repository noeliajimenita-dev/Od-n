from __future__ import annotations

from typing import Any

from src.supervisor.task import Task

from .odin_execution_engine import ExecutionResult
from .supervisor_execution_service import SupervisorExecutionService


class SupervisorExecutionController:
    """Controlador central del ciclo de ejecución de ODIN."""

    def __init__(
        self,
        execution_service: SupervisorExecutionService,
    ) -> None:
        if execution_service is None:
            raise ValueError(
                "execution_service cannot be None"
            )

        self.execution_service = execution_service

    def validate_task(self, task: Task) -> None:
        if task is None:
            raise ValueError("task cannot be None")

        if not task.task_id or not task.task_id.strip():
            raise ValueError("task_id cannot be empty")

        if not task.description or not task.description.strip():
            raise ValueError(
                "task description cannot be empty"
            )

    def assign_task(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> str:
        self.validate_task(task)

        return self.execution_service.assign(
            task=task,
            worker_id=worker_id,
        )

    def execute_task(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> ExecutionResult:
        self.validate_task(task)

        if not self.execution_service.can_execute(
            task=task,
            worker_id=worker_id,
        ):
            return ExecutionResult(
                task_id=task.task_id,
                status="error",
                worker_id=worker_id,
                error="Task cannot be executed",
            )

        return self.execution_service.execute(
            task=task,
            worker_id=worker_id,
        )

    def execute_task_with_ai(
        self,
        task: Task,
        prompt: str,
        model: str,
        worker_id: str | None = None,
        preferred_provider: str | None = None,
    ) -> ExecutionResult:
        self.validate_task(task)

        if not prompt or not prompt.strip():
            raise ValueError("prompt cannot be empty")

        if not model or not model.strip():
            raise ValueError("model cannot be empty")

        if not self.execution_service.can_execute(
            task=task,
            worker_id=worker_id,
        ):
            return ExecutionResult(
                task_id=task.task_id,
                status="error",
                worker_id=worker_id,
                error="Task cannot be executed",
            )

        return self.execution_service.execute_with_ai(
            task=task,
            prompt=prompt,
            model=model,
            worker_id=worker_id,
            preferred_provider=preferred_provider,
        )

    def status(self) -> dict[str, Any]:
        return self.execution_service.status()

    def __repr__(self) -> str:
        return (
            "SupervisorExecutionController("
            "ready=True"
            ")"
    )
