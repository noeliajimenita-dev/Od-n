from typing import Any

from src.supervisor.task import Task
from src.supervisor.task_lifecycle_manager import TaskLifecycleManager
from src.supervisor.worker_task_executor import WorkerTaskExecutor


class TaskExecutionController:
    """Coordinates the complete Supervisor task execution flow."""

    def __init__(
        self,
        lifecycle_manager: TaskLifecycleManager,
        worker_executor: WorkerTaskExecutor,
    ):
        if lifecycle_manager is None:
            raise ValueError("Task lifecycle manager is required")

        if worker_executor is None:
            raise ValueError("Worker task executor is required")

        self.lifecycle_manager = lifecycle_manager
        self.worker_executor = worker_executor

    def execute(self, task: Task, handler: Any) -> Any:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        if task.status != "assigned":
            raise ValueError(
                "Task must be assigned before execution"
            )

        self.lifecycle_manager.start(task)

        try:
            result = handler.execute(task)
            self.lifecycle_manager.complete(task, result)
            return result

        except Exception as exc:
            self.lifecycle_manager.fail(task, str(exc))
            raise

    def can_execute(self, task: Task) -> bool:
        if not isinstance(task, Task):
            return False

        return (
            task.bot_name is not None
            and task.status == "assigned"
    )
