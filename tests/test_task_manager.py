import pytest

from src.task_manager.manager import TaskManager
from src.task_manager.states import TaskState


def test_create_task():
    manager = TaskManager()

    task = manager.create_task(
        task_id="TASK-001",
        description="Crear una tarea",
    )

    assert task.task_id == "TASK-001"
    assert task.description == "Crear una tarea"
    assert task.state == TaskState.PENDING
    assert manager.count() == 1


def test_create_task_with_priority():
    manager = TaskManager()

    task = manager.create_task(
        task_id="TASK-002",
        description="Tarea prioritaria",
        priority=1,
    )

    assert task.priority == 1


def test_create_task_rejects_duplicate_id():
    manager = TaskManager()

    manager.create_task(
        task_id="TASK-003",
        description="Primera tarea",
    )

    with pytest.raises(ValueError):
        manager.create_task(
            task_id="TASK-003",
            description="Segunda tarea",
        )


def test_create_task_rejects_empty_id():
    manager = TaskManager()

    with pytest.raises(ValueError):
        manager.create_task(
            task_id="",
            description="Tarea",
        )


def test_create_task_rejects_empty_description():
    manager = TaskManager()

    with pytest.raises(ValueError):
        manager.create_task(
            task_id="TASK-004",
            description="",
        )


def test_create_task_rejects_invalid_priority():
    manager = TaskManager()

    with pytest.raises(ValueError):
        manager.create_task(
            task_id="TASK-005",
            description="Tarea",
            priority=0,
        )


def test_get_task():
    manager = TaskManager()

    manager.create_task(
        task_id="TASK-006",
        description="Buscar tarea",
    )

    task = manager.get_task("TASK-006")

    assert task is not None
    assert task.task_id == "TASK-006"


def test_get_missing_task_returns_none():
    manager = TaskManager()

    assert manager.get_task("UNKNOWN") is None


def test_get_all_tasks():
    manager = TaskManager()

    manager.create_task("TASK-007", "Primera")
    manager.create_task("TASK-008", "Segunda")

    tasks = manager.get_all_tasks()

    assert len(tasks) == 2
    assert {task.task_id for task in tasks} == {
        "TASK-007",
        "TASK-008",
    }


def test_assign_task():
    manager = TaskManager()

    manager.create_task(
        task_id="TASK-009",
        description="Asignar tarea",
    )

    task = manager.assign_task(
        task_id="TASK-009",
        worker="worker_1",
    )

    assert task.assigned_to == "worker_1"


def test_transition_task():
    manager = TaskManager()

    manager.create_task(
        task_id="TASK-010",
        description="Analizar tarea",
    )

    task = manager.transition_task(
        task_id="TASK-010",
        new_state=TaskState.ANALYZING,
    )

    assert task.state == TaskState.ANALYZING


def test_invalid_transition_is_rejected():
    manager = TaskManager()

    manager.create_task(
        task_id="TASK-011",
        description="Tarea",
    )

    with pytest.raises(ValueError):
        manager.transition_task(
            task_id="TASK-011",
            new_state=TaskState.COMPLETED,
        )


def test_set_result():
    manager = TaskManager()

    manager.create_task(
        task_id="TASK-012",
        description="Procesar resultado",
    )

    task = manager.set_result(
        task_id="TASK-012",
        result={"status": "ok"},
    )

    assert task.result == {"status": "ok"}
    assert task.error is None


def test_set_error():
    manager = TaskManager()

    manager.create_task(
        task_id="TASK-013",
        description="Provocar error controlado",
    )

    task = manager.set_error(
        task_id="TASK-013",
        error="Error de prueba",
    )

    assert task.error == "Error de prueba"


def test_missing_task_operations_raise_key_error():
    manager = TaskManager()

    with pytest.raises(KeyError):
        manager.assign_task("UNKNOWN", "worker_1")

    with pytest.raises(KeyError):
        manager.transition_task(
            "UNKNOWN",
            TaskState.ANALYZING,
        )

    with pytest.raises(KeyError):
        manager.set_result("UNKNOWN", "resultado")

    with pytest.raises(KeyError):
        manager.set_error("UNKNOWN", "error")


def test_remove_task():
    manager = TaskManager()

    manager.create_task(
        task_id="TASK-014",
        description="Eliminar tarea",
    )

    assert manager.remove_task("TASK-014") is True
    assert manager.get_task("TASK-014") is None
    assert manager.count() == 0


def test_remove_missing_task():
    manager = TaskManager()

    assert manager.remove_task("UNKNOWN") is False
