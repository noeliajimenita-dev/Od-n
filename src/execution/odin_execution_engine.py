from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from src.ai.ai_service import AIService
from src.ai.model_provider import AIRequest
from src.supervisor.task import Task
from src.workers.worker_pool import WorkerPool


@dataclass(frozen=True)
class ExecutionResult:
    task_id: str
    status: str
    worker_id: str | None = None
    output: Any = None
    error: str | None = None


class OdinExecutionEngine:
    """Motor central para ejecutar tareas de ODIN."""

    def __init__(
        self,
        worker_pool: WorkerPool,
        ai_service: AIService | None = None,
    ) -> None:
        if worker_pool is None:
            raise ValueError("worker_pool cannot be None")

        self.worker_pool = worker_pool
        self.ai_service = ai_service
        self._handlers: dict[str, Callable[[Task], Any]] = {}

    def register_handler(
        self,
        worker_id: str,
        handler: Callable[[Task], Any],
    ) -> None:
        if not worker_id or not worker_id.strip():
            raise ValueError("worker_id cannot be empty")

        if not callable(handler):
            raise TypeError("handler must be callable")

        self._handlers[worker_id.strip()] = handler

    def execute(
        self,
        task: Task,
        worker_id: str | None = None,
    ) -> ExecutionResult:
        if task is None:
            raise ValueError("task cannot be None")

        selected_worker = worker_id or task.bot_name

        if not selected_worker:
            try:
                selected_worker = self._select_worker(task)
            except Exception as exc:
                return ExecutionResult(
                    task_id=task.task_id,
                    status="failed",
                    error=str(exc),
                )

        handler = self._handlers.get(selected_worker)

        if handler is None:
            return ExecutionResult(
                task_id=task.task_id,
                status="failed",
                worker_id=selected_worker,
                error=(
                    f"No execution handler for worker: "
                    f"{selected_worker}"
                ),
            )

        task.assign(selected_worker)

        try:
            task.start()

            output = handler(task)

            task.complete(output)

            return ExecutionResult(
                task_id=task.task_id,
                status="completed",
                worker_id=selected_worker,
                output=output,
            )

        except Exception as exc:
            task.fail(str(exc))

            return ExecutionResult(
                task_id=task.task_id,
                status="failed",
                worker_id=selected_worker,
                error=str(exc),
            )

    def execute_with_ai(
        self,
        task: Task,
        prompt: str,
        model: str,
        worker_id: str | None = None,
        preferred_provider: str | None = None,
    ) -> ExecutionResult:
        if self.ai_service is None:
            return ExecutionResult(
                task_id=task.task_id,
                status="failed",
                worker_id=worker_id,
                error="AI service is not configured",
            )

        request = AIRequest(
            request_id=f"task-{task.task_id}",
            prompt=prompt,
            model=model,
        )

        try:
            response = self.ai_service.generate(
                request=request,
                preferred_provider=preferred_provider,
            )

            selected_worker = worker_id or task.bot_name

            if selected_worker:
                task.assign(selected_worker)

            task.start()
            task.complete(response.text)

            return ExecutionResult(
                task_id=task.task_id,
                status="completed",
                worker_id=selected_worker,
                output=response,
            )

        except Exception as exc:
            task.fail(str(exc))

            return ExecutionResult(
                task_id=task.task_id,
                status="failed",
                worker_id=worker_id or task.bot_name,
                error=str(exc),
            )

    def _select_worker(self, task: Task) -> str:
        """
        Selecciona un Worker utilizando el pool existente.

        El método acepta diferentes implementaciones del pool
        para mantener compatibilidad con la arquitectura actual.
        """
        required_skill = task.metadata.get(
            "required_skill"
        )

        if hasattr(self.worker_pool, "select_worker"):
            worker = self.worker_pool.select_worker(
                skill=required_skill
            )

            if worker is not None:
                return self._worker_id(worker)

        if hasattr(self.worker_pool, "select"):
            worker = self.worker_pool.select(
                skill=required_skill
            )

            if worker is not None:
                return self._worker_id(worker)

        if hasattr(self.worker_pool, "get_available_worker"):
            worker = self.worker_pool.get_available_worker(
                skill=required_skill
            )

            if worker is not None:
                return self._worker_id(worker)

        raise RuntimeError("No available worker")

    @staticmethod
    def _worker_id(worker: Any) -> str:
        if isinstance(worker, str):
            return worker

        for attribute in (
            "worker_id",
            "bot_name",
            "name",
        ):
            value = getattr(worker, attribute, None)

            if value:
                return str(value)

        raise RuntimeError(
            "Selected worker has no identifiable id"
        )

    def has_handler(self, worker_id: str) -> bool:
        return worker_id in self._handlers

    def handlers(self) -> list[str]:
        return sorted(self._handlers.keys())

    def status(self) -> dict[str, Any]:
        return {
            "registered_handlers": self.handlers(),
            "handler_count": len(self._handlers),
            "ai_enabled": self.ai_service is not None,
        }

    def clear_handlers(self) -> None:
        self._handlers.clear()
