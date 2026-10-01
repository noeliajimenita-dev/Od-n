from src.supervisor.task import Task


class TaskRepository:
    """Stores and manages Supervisor tasks."""

    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def save(self, task: Task) -> Task:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        if not task.task_id or not task.task_id.strip():
            raise ValueError("Task ID cannot be empty")

        self._tasks[task.task_id] = task
        return task

    def get(self, task_id: str) -> Task | None:
        if not task_id or not task_id.strip():
            return None

        return self._tasks.get(task_id.strip())

    def exists(self, task_id: str) -> bool:
        return self.get(task_id) is not None

    def delete(self, task_id: str) -> bool:
        if not task_id or not task_id.strip():
            return False

        return self._tasks.pop(task_id.strip(), None) is not None

    def list_tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def count(self) -> int:
        return len(self._tasks)

    def clear(self) -> None:
        self._tasks.clear()
