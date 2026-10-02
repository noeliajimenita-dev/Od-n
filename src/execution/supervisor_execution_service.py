from __future__ import annotations

from typing import Any

from src.supervisor.task import Task

from .odin_execution_engine import (
    ExecutionResult,
    OdinExecutionEngine,
)
from .worker_execution_coordinator import (
    WorkerExecutionCoordinator,
)


class SupervisorExecutionService:
    """Servicio que conecta Supervisor con la ejecución real."""

    def __init__(
        self,
        execution_engine: OdinExecutionEngine,
        coordinator: WorkerExecutionCoordinator,
    ) -> None:
        if execution_engine is None:
            raise ValueError(
                "execution_engine cannot be None"
            )

        if coordinator is None:
            raise ValueError(
                "coordinator cannot be None"
            )

        self.execution_engine = execution_engine
        self.coordinator = coordinator

    def assign(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> str:
        if task is None:
            raise ValueError("task cannot be None")

        selected_worker = self.coordinator.select_worker(
            task=task,
            worker_id=worker_id,
        )

        task.assign(selected_worker)

        return selected_worker

    def execute(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> ExecutionResult:
        if task is None:
            raise ValueError("task cannot be None")

        selected_worker = self.assign(
            task=task,
            worker_id=worker_id,
        )

        return self.execution_engine.execute(
            task=task,
            worker_id=selected_worker,
        )

    def execute_with_ai(
        self,
        task: Task,
        prompt: str,
        model: str,
        worker_id: str | None = None,
        preferred_provider: str | None = None,
    ) -> ExecutionResult:
        if task is None:
            raise ValueError("task cannot be None")

        if not prompt or not prompt.strip():
            raise ValueError("prompt cannot be empty")

        if not model or not model.strip():
            raise ValueError("model cannot be empty")

        selected_worker = self.assign(
            task=task,
            worker_id=worker_id,
        )

        return self.execution_engine.execute_with_ai(
            task=task,
            prompt=prompt,
            model=model,
            worker_id=selected_worker,
            preferred_provider=preferred_provider,
        )

    def can_execute(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> bool:
        if task is None:
            return False

        return self.coordinator.can_execute(
            task=task,
            worker_id=worker_id,
        )

    def status(self) -> dict[str, Any]:
        return {
            "execution_engine": (
                self.execution_engine.status()
            ),
            "worker_coordinator": (
                self.coordinator.status()
            ),
        }

    def __repr__(self) -> str:
        return (
            "SupervisorExecutionService("
            f"workers="
            f"{self.coordinator.registry.count()}"
            ")"
      )
