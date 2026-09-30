from src.supervisor.task import Task


class Worker1TaskReceiver:
    def __init__(self):
        self.pending_tasks: list[Task] = []

    def receive(self, task: Task) -> Task:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        if task.status != "assigned":
            raise ValueError(
                "Task must be assigned before the worker can receive it"
            )

        if task.bot_name != "worker_1":
            raise ValueError(
                "Task is not assigned to worker_1"
            )

        self.pending_tasks.append(task)

        return task

    def next_task(self) -> Task | None:
        if not self.pending_tasks:
            return None

        return self.pending_tasks.pop(0)

    def has_pending_tasks(self) -> bool:
        return bool(self.pending_tasks)
