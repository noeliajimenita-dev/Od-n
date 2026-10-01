from typing import Any


class WorkerSelector:
    """Selects an available worker according to task requirements."""

    def select(
        self,
        workers: dict[str, Any],
        required_skill: str | None = None,
    ) -> Any | None:
        if not workers:
            return None

        for worker in workers.values():
            if not self._is_available(worker):
                continue

            if required_skill is None:
                return worker

            if self._has_skill(worker, required_skill):
                return worker

        return None

    def _is_available(self, worker: Any) -> bool:
        status = getattr(worker, "status", None)

        if status is None:
            return False

        if hasattr(status, "value"):
            status = status.value

        return status == "idle"

    def _has_skill(self, worker: Any, skill: str) -> bool:
        can_handle = getattr(worker, "can_handle", None)

        if callable(can_handle):
            return bool(can_handle(skill))

        skills = getattr(worker, "skills", [])

        return skill in skills
