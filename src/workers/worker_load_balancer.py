from typing import Any


class WorkerLoadBalancer:
    """Balances tasks between available workers."""

    def select(
        self,
        workers: dict[str, Any],
        required_skill: str | None = None,
    ) -> Any | None:
        candidates = []

        for worker in workers.values():
            if not self._is_available(worker):
                continue

            if required_skill is not None and not self._has_skill(
                worker,
                required_skill,
            ):
                continue

            candidates.append(worker)

        if not candidates:
            return None

        return min(
            candidates,
            key=self._active_task_count,
        )

    def _is_available(self, worker: Any) -> bool:
        status = getattr(worker, "status", None)

        if hasattr(status, "value"):
            status = status.value

        return status == "idle"

    def _has_skill(self, worker: Any, skill: str) -> bool:
        can_handle = getattr(worker, "can_handle", None)

        if callable(can_handle):
            return bool(can_handle(skill))

        skills = getattr(worker, "skills", [])

        return skill in skills

    def _active_task_count(self, worker: Any) -> int:
        pending_tasks = getattr(worker, "pending_tasks", None)

        if pending_tasks is not None:
            return len(pending_tasks)

        current_task = getattr(worker, "current_task", None)

        return 1 if current_task is not None else 0
