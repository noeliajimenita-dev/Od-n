import pytest

from src.supervisor.task import Task
from src.supervisor.task_state_snapshot import TaskStateSnapshot


def build_task():
    task = Task(
        task_id="task-1",
        description="Process client request",
        bot_name="worker_1",
        priority=5,
        status="running",
        metadata={
            "source": "supervisor",
            "attempt": 1,
        },
    )
    return task


def test_snapshot_is_created_from_task():
    task = build_task()

    snapshot = TaskStateSnapshot.from_task(task)

    assert snapshot.task_id == "task-1"
    assert snapshot.description == "Process client request"
    assert snapshot.bot_name == "worker_1"
    assert snapshot.priority == 5
    assert snapshot.status == "running"
    assert snapshot.metadata == {
        "source": "supervisor",
        "attempt": 1,
    }


def test_snapshot_to_dict():
    snapshot = TaskStateSnapshot.from_task(build_task())

    data = snapshot.to_dict()

    assert data["task_id"] == "task-1"
    assert data["description"] == "Process client request"
    assert data["bot_name"] == "worker_1"
    assert data["priority"] == 5
    assert data["status"] == "running"
    assert data["metadata"]["attempt"] == 1


def test_snapshot_from_dict():
    data = {
        "task_id": "task-1",
        "description": "Restore task",
        "bot_name": "worker_2",
        "priority": 3,
        "status": "assigned",
        "metadata": {
            "source": "restore",
        },
    }

    snapshot = TaskStateSnapshot.from_dict(data)

    assert snapshot.task_id == "task-1"
    assert snapshot.description == "Restore task"
    assert snapshot.bot_name == "worker_2"
    assert snapshot.priority == 3
    assert snapshot.status == "assigned"
    assert snapshot.metadata["source"] == "restore"


def test_snapshot_converts_back_to_task():
    original = build_task()

    snapshot = TaskStateSnapshot.from_task(original)
    restored = snapshot.to_task()

    assert isinstance(restored, Task)
    assert restored.task_id == original.task_id
    assert restored.description == original.description
    assert restored.bot_name == original.bot_name
    assert restored.priority == original.priority
    assert restored.status == original.status
    assert restored.metadata == original.metadata


def test_snapshot_preserves_metadata_independently():
    task = build_task()

    snapshot = TaskStateSnapshot.from_task(task)
    snapshot.metadata["new_value"] = True

    assert "new_value" not in task.metadata


def test_snapshot_rejects_invalid_task():
    with pytest.raises(TypeError):
        TaskStateSnapshot.from_task("invalid-task")


def test_snapshot_rejects_invalid_data():
    with pytest.raises(TypeError):
        TaskStateSnapshot.from_dict("invalid-data")


def test_snapshot_rejects_empty_task_id():
    data = {
        "task_id": "",
        "description": "Invalid task",
    }

    with pytest.raises(ValueError):
        TaskStateSnapshot.from_dict(data)


def test_snapshot_normalizes_task_id():
    data = {
        "task_id": "  task-1  ",
        "description": "Normalized task",
    }

    snapshot = TaskStateSnapshot.from_dict(data)

    assert snapshot.task_id == "task-1"


def test_snapshot_round_trip_preserves_state():
    original = build_task()

    snapshot = TaskStateSnapshot.from_task(original)
    data = snapshot.to_dict()
    restored_snapshot = TaskStateSnapshot.from_dict(data)
    restored_task = restored_snapshot.to_task()

    assert restored_task.task_id == original.task_id
    assert restored_task.description == original.description
    assert restored_task.bot_name == original.bot_name
    assert restored_task.priority == original.priority
    assert restored_task.status == original.status
    assert restored_task.metadata == original.metadata
