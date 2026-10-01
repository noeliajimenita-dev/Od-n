from src.supervisor.task import Task
from src.supervisor.task_assignment_service import TaskAssignmentService


class TaskLifecycleManager:
    """Manages task state transitions and lifecycle events."""

    def __init__(self, assignment_service: TaskAssignmentService):
        if assignment_service is None:
            raise ValueError("Task assignment service is required")

        self.assignment_service = assignment_service

    def start(self, task: Task) -> None:
        self._validate_task(task)

        if task.bot_name is None:
            raise ValueError("Task must be assigned to a worker")

        if task.status != "assigned":
            raise ValueError(
                "Task must be assigned before it can start"
            )

        task.start()

        self.assignment_service.record_event(
            task,
            "started",
        )

    def complete(self, task: Task, result=None) -> None:
        self._validate_task(task)

        if task.status != "running":
            raise ValueError(
                "Task must be running before it can complete"
            )

        task.complete(result)

        self.assignment_service.record_event(
            task,
            "completed",
        )

    def fail(self, task: Task, error: str) -> None:
        self._validate_task(task)

        if task.status != "running":
            raise ValueError(
                "Task must be running before it can fail"
            )

        if not error or not error.strip():
            raise ValueError("Error message cannot be empty")

        task.fail(error.strip())

        self.assignment_service.record_event(
            task,
            "failed",
        )

    def _validate_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")
