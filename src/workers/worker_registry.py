from typing import Any


class WorkerRegistry:
    """Central registry for ODIN workers."""

    def __init__(self):
        self._workers: dict[str, Any] = {}

    def register(self, worker_id: str, worker: Any) -> None:
        worker_id = worker_id.strip()

        if not worker_id:
            raise ValueError("Worker ID cannot be empty")

        if worker is None:
            raise ValueError("Worker cannot be None")

        if worker_id in self._workers:
            raise ValueError(f"Worker already registered: {worker_id}")

        self._workers[worker_id] = worker

    def get(self, worker_id: str) -> Any | None:
        return self._workers.get(worker_id.strip())

    def remove(self, worker_id: str) -> Any | None:
        return self._workers.pop(worker_id.strip(), None)

    def has(self, worker_id: str) -> bool:
        return worker_id.strip() in self._workers

    def list_workers(self) -> list[str]:
        return list(self._workers.keys())

    def count(self) -> int:
        return len(self._workers)

    def clear(self) -> None:
        self._workers.clear()
