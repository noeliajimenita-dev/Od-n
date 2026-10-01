from typing import Any


class WorkerPoolStatus:
    """Provides a status snapshot for the worker pool."""

    def get_status(self, workers: dict[str, Any]) -> dict[str, Any]:
        total = len(workers)
        idle = 0
        working = 0
        paused = 0
        stopped = 0
        unknown = 0

        worker_statuses: dict[str, str] = {}

        for worker_id, worker in workers.items():
            status = getattr(worker, "status", "unknown")

            if hasattr(status, "value"):
                status = status.value

            status = str(status)
            worker_statuses[worker_id] = status

            if status == "idle":
                idle += 1
            elif status == "working":
                working += 1
            elif status == "paused":
                paused += 1
            elif status == "stopped":
                stopped += 1
            else:
                unknown += 1

        return {
            "total": total,
            "idle": idle,
            "working": working,
            "paused": paused,
            "stopped": stopped,
            "unknown": unknown,
            "available": idle > 0,
            "worker_statuses": worker_statuses,
        }

    def available_count(self, workers: dict[str, Any]) -> int:
        status = self.get_status(workers)
        return status["idle"]

    def working_count(self, workers: dict[str, Any]) -> int:
        status = self.get_status(workers)
        return status["working"]

    def is_available(self, workers: dict[str, Any]) -> bool:
        return self.available_count(workers) > 0
