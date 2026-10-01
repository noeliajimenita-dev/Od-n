from typing import Any

from src.supervisor.task import Task
from src.workers.worker_pool import WorkerPool


class SupervisorWorkerBridge:
    """Connects Supervisor tasks with the worker pool."""

    def __init__(self, worker_pool: WorkerPool):
        if worker_pool is None:
            raise ValueError("Worker pool is required")

        self.worker_pool = worker_pool

    def assign_task(
        self,
        task: Task,
        required_skill: str | None = None,
    ) -> Any:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        worker = self.worker_pool.assign_worker(
            required_skill=required_skill,
        )

        if worker is None:
            raise RuntimeError("No suitable worker available")

        worker_id = self._find_worker_id(worker)

        if worker_id is None:
            raise RuntimeError("Selected worker is not registered")

        task.assign(worker_id)

        return worker

    def _find_worker_id(self, worker: Any) -> str | None:
        for worker_id in self.worker_pool.list_workers():
            if self.worker_pool.get_worker(worker_id) is worker:
                return worker_id

        return None
