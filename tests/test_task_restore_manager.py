import pytest

from src.supervisor.task import Task
from src.supervisor.task_repository import TaskRepository
from src.supervisor.task_restore_manager import TaskRestoreManager
from src.supervisor.task_state_snapshot import TaskStateSnapshot


def build_manager():
    return TaskRestoreManager(TaskRepository())


def build_snapshot(
    task_id="task-1",
    status="running",
):
    return TaskStateSnapshot(
        task_id=task_id,
        description="Restored task",
        bot_name="worker_1",
        priority=5,
        status=status,
        metadata={
            "source": "backup",
        },
    )


def test_manager_requires_repository():
    with pytest.raises(ValueError):
        TaskRestoreManager(None)


def test_manager_restores_task():
    manager = build_manager()
    snapshot = build_snapshot()

    task = manager.restore(snapshot)

    assert isinstance(task, Task)
    assert task.task_id == "task-1"
    assert task.description == "Restored task"
    assert task.bot_name == "worker_1"
    assert task.priority == 5
    assert task.status == "running"


def test_manager_stores_restored_task():
    manager = build_manager()

    manager.restore(build_snapshot())

    restored = manager.get_restored("task-1")

    assert restored is not None
    assert restored.task_id == "task-1"


def test_manager_restores_only_if_missing():
    manager = build_manager()

    original = manager.restore(
        build_snapshot(
            task_id="task-1",
            status="pending",
        )
    )

    snapshot = build_snapshot(
        task_id="task-1",
        status="completed",
    )

    result = manager.restore_if_missing(snapshot)

    assert result is original
    assert result.status == "pending"


def test_manager_restores_missing_task():
    manager = build_manager()

    snapshot = build_snapshot(
        task_id="missing-task",
        status="assigned",
    )

    task = manager.restore_if_missing(snapshot)

    assert task.task_id == "missing-task"
    assert task.status == "assigned"


def test_manager_validates_restorable_snapshot():
    manager = build_manager()

    snapshot = build_snapshot()

    assert manager.is_restorable(snapshot) is True


def test_manager_rejects_invalid_snapshot_for_restore():
    manager = build_manager()

    with pytest.raises(TypeError):
        manager.restore("invalid-snapshot")


def test_manager_invalid_snapshot_is_not_restorable():
    manager = build_manager()

    assert manager.is_restorable("invalid-snapshot") is False


def test_manager_restores_multiple_tasks():
    manager = build_manager()

    snapshots = [
        build_snapshot("task-1", "pending"),
        build_snapshot("task-2", "assigned"),
        build_snapshot("task-3", "completed"),
    ]

    tasks = manager.restore_many(snapshots)

    assert len(tasks) == 3
    assert [task.task_id for task in tasks] == [
        "task-1",
        "task-2",
        "task-3",
    ]


def test_manager_rejects_missing_snapshot_list():
    manager = build_manager()

    with pytest.raises(ValueError):
        manager.restore_many(None)


def test_manager_preserves_metadata():
    manager = build_manager()

    task = manager.restore(build_snapshot())

    assert task.metadata == {
        "source": "backup",
    }


def test_manager_returns_none_for_unknown_task():
    manager = build_manager()

    assert manager.get_restored("unknown") is None


def test_manager_restoration_replaces_existing_task():
    manager = build_manager()

    manager.restore(
        build_snapshot(
            task_id="task-1",
            status="pending",
        )
    )

    manager.restore(
        build_snapshot(
            task_id="task-1",
            status="completed",
        )
    )

    restored = manager.get_restored("task-1")

    assert restored.status == "completed"
