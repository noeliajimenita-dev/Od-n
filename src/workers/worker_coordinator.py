from typing import Any

from .worker_load_balancer import WorkerLoadBalancer
from .worker_registry import WorkerRegistry
from .worker_selector import WorkerSelector


class WorkerCoordinator:
    """Coordinates the ODIN worker pool."""

    def __init__(
        self,
        registry: WorkerRegistry | None = None,
        selector: WorkerSelector | None = None,
        load_balancer: WorkerLoadBalancer | None = None,
    ):
        self.registry = registry or WorkerRegistry()
        self.selector = selector or WorkerSelector()
        self.load_balancer = load_balancer or WorkerLoadBalancer()

    def register_worker(self, worker_id: str, worker: Any) -> None:
        self.registry.register(worker_id, worker)

    def get_worker(self, worker_id: str) -> Any | None:
        return self.registry.get(worker_id)

    def select_worker(self, required_skill: str | None = None) -> Any | None:
        workers = {
            worker_id: self.registry.get(worker_id)
            for worker_id in self.registry.list_workers()
        }

        return self.selector.select(
            workers,
            required_skill=required_skill,
        )

    def assign_worker(self, required_skill: str | None = None) -> Any | None:
        workers = {
            worker_id: self.registry.get(worker_id)
            for worker_id in self.registry.list_workers()
        }

        return self.load_balancer.select(
            workers,
            required_skill=required_skill,
        )

    def remove_worker(self, worker_id: str) -> Any | None:
        return self.registry.remove(worker_id)

    def list_workers(self) -> list[str]:
        return self.registry.list_workers()

    def worker_count(self) -> int:
        return self.registry.count()
