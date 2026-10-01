from src.supervisor.task import Task
from src.supervisor.task_repository import TaskRepository
from src.supervisor.task_state_snapshot import TaskStateSnapshot


class TaskRecoveryService:
    """Recovers Supervisor tasks from persisted snapshots."""

    def __init__(self, repository: TaskRepository):
        if repository is None:
            raise ValueError("Task repository is required")

        self.repository = repository

    def recover(self, snapshot: TaskStateSnapshot) -> Task:
        if not isinstance(snapshot, TaskStateSnapshot):
            raise TypeError("Expected a TaskStateSnapshot")

        task = snapshot.to_task()
        self.repository.save(task)
        return task

    def recover_from_dict(self, data: dict) -> Task:
        snapshot = TaskStateSnapshot.from_dict(data)
        return self.recover(snapshot)

    def recover_all(
        self,
        snapshots: list[TaskStateSnapshot],
    ) -> list[Task]:
        if snapshots is None:
            raise ValueError("Snapshots are required")

        recovered_tasks = []

        for snapshot in snapshots:
            recovered_tasks.append(self.recover(snapshot))

        return recovered_tasks

    def get_recovered(self, task_id: str) -> Task | None:
        return self.repository.get(task_id)

    def count_recovered(self) -> int:
        return self.repository.count()
