from typing import Any

from src.supervisor.task import Task
from src.supervisor.task_assignment_log import TaskAssignmentLog
from src.supervisor.task_assignment_manager import TaskAssignmentManager


class TaskAssignmentService:
    """Coordinates task assignment tracking and event logging."""

    def __init__(
        self,
        manager: TaskAssignmentManager,
        assignment_log: TaskAssignmentLog | None = None,
    ):
        if manager is None:
            raise ValueError("Task assignment manager is required")

        self.manager = manager
        self.assignment_log = assignment_log or TaskAssignmentLog()

    def assign(
        self,
        task: Task,
        required_skill: str | None = None,
    ) -> Any:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        worker = self.manager.assign(
            task,
            required_skill=required_skill,
        )

        if task.bot_name is None:
            raise RuntimeError("Task was not assigned to a worker")

        self.assignment_log.record(
            task.task_id,
            task.bot_name,
            "assigned",
        )

        return worker

    def record_event(
        self,
        task: Task,
        event: str,
    ):
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        if task.bot_name is None:
            raise RuntimeError("Task has no assigned worker")

        return self.assignment_log.record(
            task.task_id,
            task.bot_name,
            event,
        )

    def get_assignment(self, task_id: str) -> str | None:
        return self.manager.get_assignment(task_id)

    def get_task_events(self, task_id: str):
        return self.assignment_log.task_events(task_id)

    def get_worker_events(self, worker_id: str):
        return self.assignment_log.worker_events(worker_id)

    def assignment_count(self) -> int:
        return self.manager.count()

    def event_count(self) -> int:
        return self.assignment_log.count()
