from __future__ import annotations

from typing import Any

from src.supervisor.task import Task

from .worker_execution_registry import WorkerExecutionRegistry


class WorkerExecutionCoordinator:
    """Coordina la ejecución de tareas entre Workers."""

    def __init__(
        self,
        registry: WorkerExecutionRegistry,
    ) -> None:
        if registry is None:
            raise ValueError("registry cannot be None")

        self.registry = registry

    def select_worker(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> str:
        if task is None:
            raise ValueError("task cannot be None")

        selected = (
            worker_id
            or task.bot_name
            or self._worker_from_metadata(task)
        )

        if selected:
            adapter = self.registry.get(selected)

            if adapter is None:
                raise RuntimeError(
                    f"Worker not registered: {selected}"
                )

            return selected

        available = self.registry.available_workers()

        if not available:
            raise RuntimeError(
                "No available worker"
            )

        return available[0]

    @staticmethod
    def _worker_from_metadata(
        task: Task,
    ) -> str | None:
        metadata = task.metadata or {}

        for key in (
            "worker_id",
            "bot_name",
            "assigned_worker",
        ):
            value = metadata.get(key)

            if value and str(value).strip():
                return str(value).strip()

        return None

    def execute(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> Any:
        selected_worker = self.select_worker(
            task=task,
            worker_id=worker_id,
        )

        adapter = self.registry.require(
            selected_worker
        )

        task.assign(selected_worker)

        return adapter.execute(task)

    def can_execute(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> bool:
        try:
            selected_worker = self.select_worker(
                task=task,
                worker_id=worker_id,
            )

            adapter = self.registry.require(
                selected_worker
            )

            return adapter.has_execution_interface()

        except (RuntimeError, KeyError, ValueError):
            return False

    def get_worker_status(
        self,
        worker_id: str,
    ) -> dict[str, Any]:
        return self.registry.require(
            worker_id
        ).status()

    def status(self) -> dict[str, Any]:
        return {
            "registered_workers": self.registry.count(),
            "available_workers": (
                self.registry.available_workers()
            ),
            "executable_workers": (
                self.registry.executable_workers()
            ),
        }
