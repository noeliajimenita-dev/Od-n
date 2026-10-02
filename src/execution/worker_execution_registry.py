from __future__ import annotations

from typing import Any

from .worker_execution_adapter import WorkerExecutionAdapter


class WorkerExecutionRegistry:
    """Registro central de Workers preparados para ejecución."""

    def __init__(self) -> None:
        self._workers: dict[str, WorkerExecutionAdapter] = {}

    def register(
        self,
        adapter: WorkerExecutionAdapter,
    ) -> None:
        if not isinstance(
            adapter,
            WorkerExecutionAdapter,
        ):
            raise TypeError(
                "adapter must be a WorkerExecutionAdapter"
            )

        if adapter.worker_id in self._workers:
            raise ValueError(
                f"Worker already registered: "
                f"{adapter.worker_id}"
            )

        self._workers[adapter.worker_id] = adapter

    def replace(
        self,
        adapter: WorkerExecutionAdapter,
    ) -> None:
        if not isinstance(
            adapter,
            WorkerExecutionAdapter,
        ):
            raise TypeError(
                "adapter must be a WorkerExecutionAdapter"
            )

        self._workers[adapter.worker_id] = adapter

    def get(
        self,
        worker_id: str,
    ) -> WorkerExecutionAdapter | None:
        if not worker_id or not worker_id.strip():
            return None

        return self._workers.get(
            worker_id.strip()
        )

    def require(
        self,
        worker_id: str,
    ) -> WorkerExecutionAdapter:
        adapter = self.get(worker_id)

        if adapter is None:
            raise KeyError(
                f"Worker not registered: {worker_id}"
            )

        return adapter

    def exists(
        self,
        worker_id: str,
    ) -> bool:
        return self.get(worker_id) is not None

    def remove(
        self,
        worker_id: str,
    ) -> bool:
        worker_id = worker_id.strip()

        if worker_id not in self._workers:
            return False

        del self._workers[worker_id]
        return True

    def list_workers(self) -> list[str]:
        return sorted(self._workers.keys())

    def count(self) -> int:
        return len(self._workers)

    def available_workers(self) -> list[str]:
        available: list[str] = []

        for worker_id, adapter in self._workers.items():
            status = adapter.status()

            if status.get("available", True):
                available.append(worker_id)

        return sorted(available)

    def executable_workers(self) -> list[str]:
        return sorted(
            worker_id
            for worker_id, adapter in self._workers.items()
            if adapter.has_execution_interface()
        )

    def status(
        self,
        worker_id: str | None = None,
    ) -> dict[str, Any]:
        if worker_id is not None:
            adapter = self.require(worker_id)

            return adapter.status()

        return {
            worker_id: adapter.status()
            for worker_id, adapter in self._workers.items()
        }

    def clear(self) -> None:
        self._workers.clear()

    def __len__(self) -> int:
        return self.count()

    def __repr__(self) -> str:
        return (
            f"WorkerExecutionRegistry("
            f"workers={self.count()}"
            ")"
          )
