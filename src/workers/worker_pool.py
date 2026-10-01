from typing import Any

from .worker_coordinator import WorkerCoordinator
from .worker_pool_status import WorkerPoolStatus


class WorkerPool:
    """Unified interface for managing the ODIN worker pool."""

    def __init__(
        self,
        coordinator: WorkerCoordinator | None = None,
        status_manager: WorkerPoolStatus | None = None,
    ):
        self.coordinator = coordinator or WorkerCoordinator()
        self.status_manager = status_manager or WorkerPoolStatus()

    def add_worker(self, worker_id: str, worker: Any) -> None:
        self.coordinator.register_worker(worker_id, worker)

    def remove_worker(self, worker_id: str) -> Any | None:
        return self.coordinator.remove_worker(worker_id)

    def get_worker(self, worker_id: str) -> Any | None:
        return self.coordinator.get_worker(worker_id)

    def select_worker(self, required_skill: str | None = None) -> Any | None:
        return self.coordinator.select_worker(required_skill)

    def assign_worker(self, required_skill: str | None = None) -> Any | None:
        return self.coordinator.assign_worker(required_skill)

    def status(self) -> dict[str, Any]:
        workers = {
            worker_id: self.coordinator.get_worker(worker_id)
            for worker_id in self.coordinator.list_workers()
        }

        return self.status_manager.get_status(workers)

    def list_workers(self) -> list[str]:
        return self.coordinator.list_workers()

    def count(self) -> int:
        return self.coordinator.worker_count()

    def has_available_worker(self) -> bool:
        return self.status()["available"]
