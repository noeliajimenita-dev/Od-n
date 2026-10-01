from src.supervisor.task import Task
from src.supervisor.task_repository import TaskRepository
from src.supervisor.task_state_snapshot import TaskStateSnapshot


class TaskRestoreManager:
    """Manages restoration of Supervisor tasks from snapshots."""

    def __init__(self, repository: TaskRepository):
        if repository is None:
            raise ValueError("Task repository is required")

        self.repository = repository

    def restore(self, snapshot: TaskStateSnapshot) -> Task:
        if not isinstance(snapshot, TaskStateSnapshot):
            raise TypeError("Expected a TaskStateSnapshot")

        task = snapshot.to_task()
        self.repository.save(task)
        return task

    def restore_if_missing(
        self,
        snapshot: TaskStateSnapshot,
    ) -> Task:
        if not isinstance(snapshot, TaskStateSnapshot):
            raise TypeError("Expected a TaskStateSnapshot")

        existing = self.repository.get(snapshot.task_id)

        if existing is not None:
            return existing

        return self.restore(snapshot)

    def is_restorable(self, snapshot: TaskStateSnapshot) -> bool:
        if not isinstance(snapshot, TaskStateSnapshot):
            return False

        return bool(snapshot.task_id.strip())

    def get_restored(self, task_id: str) -> Task | None:
        return self.repository.get(task_id)

    def restore_many(
        self,
        snapshots: list[TaskStateSnapshot],
    ) -> list[Task]:
        if snapshots is None:
            raise ValueError("Snapshots are required")

        restored_tasks = []

        for snapshot in snapshots:
            restored_tasks.append(self.restore(snapshot))

        return restored_tasks
