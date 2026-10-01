from src.supervisor.task import Task
from src.supervisor.task_repository import TaskRepository


class TaskPersistenceService:
    """Provides a controlled persistence interface for Supervisor tasks."""

    def __init__(self, repository: TaskRepository):
        if repository is None:
            raise ValueError("Task repository is required")

        self.repository = repository

    def save(self, task: Task) -> Task:
        self._validate_task(task)
        return self.repository.save(task)

    def get(self, task_id: str) -> Task | None:
        return self.repository.get(task_id)

    def exists(self, task_id: str) -> bool:
        return self.repository.exists(task_id)

    def update(self, task: Task) -> Task:
        self._validate_task(task)

        if not self.repository.exists(task.task_id):
            raise ValueError(f"Task not found: {task.task_id}")

        return self.repository.save(task)

    def delete(self, task_id: str) -> bool:
        return self.repository.delete(task_id)

    def list_tasks(self) -> list[Task]:
        return self.repository.list_tasks()

    def count(self) -> int:
        return self.repository.count()

    def clear(self) -> None:
        self.repository.clear()

    def _validate_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")
