from typing import Any

from src.supervisor.task import Task


class Worker3TaskExecutor:
    def execute(
        self,
        task: Task,
        handler: Any,
    ) -> Any:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        if task.bot_name != "worker_3":
            raise ValueError(
                "Task is not assigned to worker_3"
            )

        if task.status != "assigned":
            raise ValueError(
                "Task must be assigned before execution"
            )

        if handler is None or not hasattr(handler, "execute"):
            raise ValueError(
                "A valid execution handler is required"
            )

        task.start()

        try:
            result = handler.execute(task)
            task.complete(result)
            return result

        except Exception as exc:
            task.fail(str(exc))
            raise
