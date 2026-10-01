from src.supervisor.task import Task
from src.supervisor.task_repository import TaskRepository
from src.supervisor.task_state_snapshot import TaskStateSnapshot


class TaskPersistenceSnapshotService:
    """Coordinates task snapshots with task persistence."""

    def __init__(self, repository: TaskRepository):
        if repository is None:
            raise ValueError("Task repository is required")

        self.repository = repository

    def create_snapshot(self, task: Task) -> TaskStateSnapshot:
        if not isinstance(task, Task):
            raise TypeError("Expected a Task instance")

        return TaskStateSnapshot.from_task(task)

    def save_snapshot(self, snapshot: TaskStateSnapshot) -> Task:
        if not isinstance(snapshot, TaskStateSnapshot):
            raise TypeError("Expected a TaskStateSnapshot")

        task = snapshot.to_task()
        self.repository.save(task)
        return task

    def save_task_snapshot(self, task: Task) -> TaskStateSnapshot:
        snapshot = self.create_snapshot(task)
        self.save_snapshot(snapshot)
        return snapshot

    def get_snapshot(self, task_id: str) -> TaskStateSnapshot | None:
        task = self.repository.get(task_id)

        if task is None:
            return None

        return TaskStateSnapshot.from_task(task)

    def list_snapshots(self) -> list[TaskStateSnapshot]:
        return [
            TaskStateSnapshot.from_task(task)
            for task in self.repository.list_tasks()
        ]

    def count_snapshots(self) -> int:
        return self.repository.count()
