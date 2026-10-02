from __future__ import annotations

from typing import Any, Callable

from src.supervisor.task import Task


class WorkerExecutionAdapter:
    """Adaptador uniforme para ejecutar tareas en Workers."""

    def __init__(
        self,
        worker_id: str,
        worker: Any,
    ) -> None:
        if not worker_id or not worker_id.strip():
            raise ValueError("worker_id cannot be empty")

        if worker is None:
            raise ValueError("worker cannot be None")

        self.worker_id = worker_id.strip()
        self.worker = worker

    def execute(self, task: Task) -> Any:
        if task is None:
            raise ValueError("task cannot be None")

        task.assign(self.worker_id)

        executor = getattr(self.worker, "execute", None)

        if callable(executor):
            return executor(task)

        accept_task = getattr(
            self.worker,
            "accept_task",
            None,
        )

        if callable(accept_task):
            accepted = accept_task(task)

            if accepted is False:
                raise RuntimeError(
                    f"Worker rejected task: {task.task_id}"
                )

            return self._execute_from_queue(task)

        raise RuntimeError(
            f"Worker {self.worker_id} has no execution interface"
        )

    def _execute_from_queue(self, task: Task) -> Any:
        execute_next = getattr(
            self.worker,
            "execute_next",
            None,
        )

        if callable(execute_next):
            return execute_next()

        process_task = getattr(
            self.worker,
            "process_task",
            None,
        )

        if callable(process_task):
            return process_task(task)

        raise RuntimeError(
            f"Worker {self.worker_id} accepted the task "
            "but has no execution method"
        )

    def status(self) -> dict[str, Any]:
        worker_status = getattr(
            self.worker,
            "status",
            None,
        )

        if callable(worker_status):
            status = worker_status()

            if isinstance(status, dict):
                return {
                    "worker_id": self.worker_id,
                    **status,
                }

        return {
            "worker_id": self.worker_id,
            "available": True,
        }

    def has_execution_interface(self) -> bool:
        return any(
            callable(getattr(self.worker, name, None))
            for name in (
                "execute",
                "accept_task",
                "process_task",
                "execute_next",
            )
        )

    def __repr__(self) -> str:
        return (
            f"WorkerExecutionAdapter("
            f"worker_id={self.worker_id!r}"
            ")"
      )
