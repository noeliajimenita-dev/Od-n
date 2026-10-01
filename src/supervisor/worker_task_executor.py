from typing import Any

from src.supervisor.task import Task
from src.supervisor.task_assignment_service import TaskAssignmentService


class WorkerTaskExecutor:
    """Executes assigned Supervisor tasks through their workers."""

    def __init__(self, assignment_service: TaskAssignmentService):
        if assignment_service is None:
            raise ValueError("Task assignment service is required")

        self.assignment_service = assignment_service

    def execute(self, task: Task, handler: Any) -> Any:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        if task.bot_name is None:
            raise ValueError("Task must be assigned to a worker")

        if handler is None or not hasattr(handler, "execute"):
            raise ValueError("A valid execution handler is required")

        task.start()

        self.assignment_service.record_event(
            task,
            "started",
        )

        try:
            result = handler.execute(task)

            task.complete(result)

            self.assignment_service.record_event(
                task,
                "completed",
            )

            return result

        except Exception as exc:
            task.fail(str(exc))

            self.assignment_service.record_event(
                task,
                "failed",
            )

            raise
