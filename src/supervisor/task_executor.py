from typing import Any

from .task import Task


class TaskExecutor:
    def __init__(self, bot_handlers: dict[str, Any] | None = None):
        self.bot_handlers = bot_handlers or {}

    def execute(self, task: Task) -> Any:
        if task.bot_name is None:
            raise ValueError("Task has no assigned bot")

        handler = self.bot_handlers.get(task.bot_name)

        if handler is None:
            raise ValueError(
                f"No handler available for bot: {task.bot_name}"
            )

        task.start()

        try:
            result = handler.execute(task)
            task.complete(result)
            return result

        except Exception as exc:
            task.fail(str(exc))
            raise
