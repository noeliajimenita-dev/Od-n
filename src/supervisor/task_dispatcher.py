from .task import Task


class TaskDispatcher:
    def __init__(self, available_bots: list[str] | None = None):
        self.available_bots = available_bots or []

    def dispatch(self, task: Task, bot_name: str | None = None) -> Task:
        selected_bot = bot_name or self._select_bot()

        if selected_bot is None:
            raise ValueError("No available bot for task")

        if selected_bot not in self.available_bots:
            raise ValueError(f"Bot not available: {selected_bot}")

        task.assign(selected_bot)

        return task

    def _select_bot(self) -> str | None:
        if not self.available_bots:
            return None

        return self.available_bots[0]
