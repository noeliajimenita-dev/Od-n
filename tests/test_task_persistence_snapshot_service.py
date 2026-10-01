import pytest

from src.supervisor.task import Task
from src.supervisor.task_persistence_snapshot_service import (
    TaskPersistenceSnapshotService,
)
from src.supervisor.task_repository import TaskRepository
from src.supervisor.task_state_snapshot import TaskStateSnapshot


def build_service():
    return TaskPersistenceSnapshotService(TaskRepository())


def build_task(task_id="task-1"):
    return Task(
        task_id=task_id,
        description="Persistent task",
        bot_name="worker_1",
        priority=3,
        status="running",
        metadata={"source": "test"},
    )


def test_service_requires_repository():
    with pytest.raises(ValueError):
        TaskPersistenceSnapshotService(None)


def test_service_creates_snapshot():
    service = build_service()
    task = build_task()

    snapshot = service.create_snapshot(task)

    assert isinstance(snapshot, TaskStateSnapshot)
    assert snapshot.task_id == "task-1"
    assert snapshot.status == "running"


def test_service_rejects_invalid_task():
    service = build_service()

    with pytest.raises(TypeError):
        service.create_snapshot("invalid-task")


def test_service_saves_snapshot():
    service = build_service()
    snapshot = TaskStateSnapshot.from_task(build_task())

    task = service.save_snapshot(snapshot)

    assert isinstance(task, Task)
    assert task.task_id == "task-1"
    assert service.count_snapshots() == 1


def test_service_rejects_invalid_snapshot():
    service = build_service()

    with pytest.raises(TypeError):
        service.save_snapshot("invalid-snapshot")


def test_service_saves_task_snapshot():
    service = build_service()
    task = build_task()

    snapshot = service.save_task_snapshot(task)

    assert isinstance(snapshot, TaskStateSnapshot)
    assert snapshot.task_id == task.task_id
    assert service.count_snapshots() == 1


def test_service_gets_snapshot():
    service = build_service()
    service.save_task_snapshot(build_task())

    snapshot = service.get_snapshot("task-1")

    assert snapshot is not None
    assert snapshot.task_id == "task-1"
    assert snapshot.description == "Persistent task"


def test_service_returns_none_for_missing_snapshot():
    service = build_service()

    assert service.get_snapshot("missing") is None


def test_service_lists_snapshots():
    service = build_service()

    service.save_task_snapshot(build_task("task-1"))
    service.save_task_snapshot(build_task("task-2"))

    snapshots = service.list_snapshots()

    assert len(snapshots) == 2
    assert [snapshot.task_id for snapshot in snapshots] == [
        "task-1",
        "task-2",
    ]


def test_service_counts_snapshots():
    service = build_service()

    service.save_task_snapshot(build_task("task-1"))
    service.save_task_snapshot(build_task("task-2"))

    assert service.count_snapshots() == 2


def test_service_preserves_task_metadata():
    service = build_service()
    task = build_task()

    snapshot = service.save_task_snapshot(task)

    assert snapshot.metadata == {
        "source": "test",
    }


def test_service_updates_snapshot_for_same_task():
    service = build_service()

    first = build_task("task-1")
    first.status = "pending"

    second = build_task("task-1")
    second.status = "completed"

    service.save_task_snapshot(first)
    service.save_task_snapshot(second)

    snapshot = service.get_snapshot("task-1")

    assert snapshot.status == "completed"
    assert service.count_snapshots() == 1
