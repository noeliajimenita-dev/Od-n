import pytest

from src.supervisor.task import Task
from src.supervisor.task_recovery_service import TaskRecoveryService
from src.supervisor.task_repository import TaskRepository
from src.supervisor.task_state_snapshot import TaskStateSnapshot


def build_service():
    repository = TaskRepository()
    return TaskRecoveryService(repository)


def build_snapshot(
    task_id="task-1",
    status="running",
):
    return TaskStateSnapshot(
        task_id=task_id,
        description="Recovered task",
        bot_name="worker_1",
        priority=4,
        status=status,
        metadata={
            "source": "snapshot",
        },
    )


def test_service_requires_repository():
    with pytest.raises(ValueError):
        TaskRecoveryService(None)


def test_service_recovers_task_from_snapshot():
    service = build_service()
    snapshot = build_snapshot()

    task = service.recover(snapshot)

    assert isinstance(task, Task)
    assert task.task_id == "task-1"
    assert task.description == "Recovered task"
    assert task.bot_name == "worker_1"
    assert task.priority == 4
    assert task.status == "running"


def test_service_stores_recovered_task():
    service = build_service()
    snapshot = build_snapshot()

    service.recover(snapshot)

    recovered = service.get_recovered("task-1")

    assert recovered is not None
    assert recovered.task_id == "task-1"


def test_service_recovers_from_dictionary():
    service = build_service()

    data = {
        "task_id": "task-2",
        "description": "Dictionary task",
        "bot_name": "worker_2",
        "priority": 2,
        "status": "assigned",
        "metadata": {
            "source": "dictionary",
        },
    }

    task = service.recover_from_dict(data)

    assert isinstance(task, Task)
    assert task.task_id == "task-2"
    assert task.description == "Dictionary task"
    assert task.bot_name == "worker_2"
    assert task.status == "assigned"


def test_service_recovers_multiple_tasks():
    service = build_service()

    snapshots = [
        build_snapshot("task-1"),
        build_snapshot("task-2", "assigned"),
        build_snapshot("task-3", "pending"),
    ]

    tasks = service.recover_all(snapshots)

    assert len(tasks) == 3
    assert [task.task_id for task in tasks] == [
        "task-1",
        "task-2",
        "task-3",
    ]


def test_service_counts_recovered_tasks():
    service = build_service()

    service.recover(build_snapshot("task-1"))
    service.recover(build_snapshot("task-2"))

    assert service.count_recovered() == 2


def test_service_rejects_invalid_snapshot():
    service = build_service()

    with pytest.raises(TypeError):
        service.recover("invalid-snapshot")


def test_service_rejects_missing_snapshots():
    service = build_service()

    with pytest.raises(ValueError):
        service.recover_all(None)


def test_service_preserves_metadata():
    service = build_service()

    snapshot = build_snapshot()

    task = service.recover(snapshot)

    assert task.metadata == {
        "source": "snapshot",
    }


def test_service_replaces_existing_task_with_same_id():
    service = build_service()

    first = build_snapshot("task-1", "pending")
    second = build_snapshot("task-1", "completed")

    service.recover(first)
    service.recover(second)

    recovered = service.get_recovered("task-1")

    assert recovered.status == "completed"
    assert service.count_recovered() == 1


def test_service_missing_task_returns_none():
    service = build_service()

    assert service.get_recovered("missing") is None
