from typing import Any

from src.supervisor.task import Task
from src.supervisor.task_router import SupervisorTaskRouter


class TaskAssignmentManager:
    """Manages task assignments between the Supervisor and workers."""

    def __init__(self, router: SupervisorTaskRouter):
        if router is None:
            raise ValueError("Task router is required")

        self.router = router
        self.assignments: dict[str, str] = {}

    def assign(
        self,
        task: Task,
        required_skill: str | None = None,
    ) -> Any:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        if required_skill is not None:
            worker = self.router.route_with_skill(
                task,
                required_skill,
            )
        else:
            worker = self.router.route(task)

        if task.bot_name is None:
            raise RuntimeError("Task was not assigned to a worker")

        self.assignments[task.task_id] = task.bot_name

        return worker

    def get_assignment(self, task_id: str) -> str | None:
        return self.assignments.get(task_id)

    def is_assigned(self, task_id: str) -> bool:
        return task_id in self.assignments

    def remove_assignment(self, task_id: str) -> str | None:
        return self.assignments.pop(task_id, None)

    def list_assignments(self) -> dict[str, str]:
        return dict(self.assignments)

    def count(self) -> int:
        return len(self.assignments)
