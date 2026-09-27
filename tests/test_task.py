from datetime import datetime

import pytest

from src.task_manager.states import TaskState
from src.task_manager.task import Task


def test_task_creation():
    task = Task(
        task_id="TASK-001",
        description="Crear una prueba",
    )

    assert task.task_id == "TASK-001"
    assert task.description == "Crear una prueba"
    assert task.state == TaskState.PENDING
    assert task.priority == 5
    assert task.assigned_to is None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_assign():
    task = Task(
        task_id="TASK-002",
        description="Tarea de prueba",
    )

    task.assign("worker_1")

    assert task.assigned_to == "worker_1"


def test_task_assign_rejects_empty_worker():
    task = Task(
        task_id="TASK-003",
        description="Tarea de prueba",
    )

    with pytest.raises(ValueError):
        task.assign("")


def test_task_update_state():
    task = Task(
        task_id="TASK-004",
        description="Tarea de prueba",
    )

    task.update_state(TaskState.ANALYZING)

    assert task.state == TaskState.ANALYZING


def test_task_set_result():
    task = Task(
        task_id="TASK-005",
        description="Tarea de prueba",
    )

    task.set_error("Error temporal")
    task.set_result({"status": "ok"})

    assert task.result == {"status": "ok"}
    assert task.error is None


def test_task_set_error():
    task = Task(
        task_id="TASK-006",
        description="Tarea de prueba",
    )

    task.set_error("Fallo de prueba")

    assert task.error == "Fallo de prueba"


def test_task_set_error_rejects_empty_error():
    task = Task(
        task_id="TASK-007",
        description="Tarea de prueba",
    )

    with pytest.raises(ValueError):
        task.set_error("")


def test_task_is_finished():
    task = Task(
        task_id="TASK-008",
        description="Tarea de prueba",
    )

    assert task.is_finished() is False

    task.update_state(TaskState.COMPLETED)

    assert task.is_finished() is True


def test_stopped_task_is_finished():
    task = Task(
        task_id="TASK-009",
        description="Tarea de prueba",
    )

    task.update_state(TaskState.STOPPED)

    assert task.is_finished() is True


def test_task_to_dict():
    task = Task(
        task_id="TASK-010",
        description="Tarea de prueba",
        priority=2,
    )

    task.assign("worker_2")

    data = task.to_dict()

    assert data["task_id"] == "TASK-010"
    assert data["description"] == "Tarea de prueba"
    assert data["state"] == "PENDING"
    assert data["priority"] == 2
    assert data["assigned_to"] == "worker_2"
    assert "created_at" in data
    assert "updated_at" in data
    assert "metadata" in data
