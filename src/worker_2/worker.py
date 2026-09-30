from src.supervisor.task import Task


class Worker2:
    def __init__(
        self,
        worker_id: str = "worker_2",
        skills: list[str] | None = None,
    ):
        self.worker_id = worker_id
        self.skills = skills or []
        self.status = "idle"
        self.current_task: Task | None = None

    def can_handle(self, skill: str) -> bool:
        return skill in self.skills

    def accept_task(self, task: Task) -> None:
        if self.status != "idle":
            raise RuntimeError("Worker is not available")

        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        self.current_task = task
        self.status = "working"

    def complete_task(self) -> Task:
        if self.current_task is None:
            raise RuntimeError("Worker has no active task")

        task = self.current_task
        self.current_task = None
        self.status = "idle"

        return task

    def pause(self) -> None:
        if self.current_task is not None:
            raise RuntimeError(
                "Cannot pause worker while a task is active"
            )

        self.status = "paused"

    def resume(self) -> None:
        self.status = "idle"
