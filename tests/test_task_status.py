from src.task_manager.manager import TaskManager
from src.task_manager.states import TaskState
from src.task_manager.status import get_task_status


def test_empty_task_status():
    manager = TaskManager()

    status = get_task_status(manager)

    assert status["total_tasks"] == 0
    assert status["active_tasks"] == 0
    assert status["active_task_ids"] == []
    assert status["completed_tasks"] == 0
    assert status["paused_tasks"] == 0
    assert status["stopped_tasks"] == 0
    assert status["error_tasks"] == 0
    assert status["resource_limited_tasks"] == 0
    assert status["by_state"] == {}


def test_task_status_counts_states():
    manager = TaskManager()

    manager.create_task("TASK-001", "Analizar")
    manager.create_task("TASK-002", "Trabajar")
    manager.create_task("TASK-003", "Finalizar")

    manager.transition_task(
        "TASK-001",
        TaskState.ANALYZING,
    )

    manager.transition_task(
        "TASK-002",
        TaskState.ANALYZING,
    )
    manager.transition_task(
        "TASK-002",
        TaskState.WORKING,
    )

    manager.transition_task(
        "TASK-003",
        TaskState.ANALYZING,
    )
    manager.transition_task(
        "TASK-003",
        TaskState.PROPOSING,
    )
    manager.transition_task(
        "TASK-003",
        TaskState.WORKING,
    )
    manager.transition_task(
        "TASK-003",
        TaskState.TESTING,
    )
    manager.transition_task(
        "TASK-003",
        TaskState.COMPLETED,
    )

    status = get_task_status(manager)

    assert status["total_tasks"] == 3
    assert status["active_tasks"] == 2
    assert status["completed_tasks"] == 1


def test_active_task_ids():
    manager = TaskManager()

    manager.create_task("TASK-004", "Activa")
    manager.create_task("TASK-005", "Pendiente")

    manager.transition_task(
        "TASK-004",
        TaskState.ANALYZING,
    )

    status = get_task_status(manager)

    assert status["active_task_ids"] == ["TASK-004"]


def test_paused_task_count():
    manager = TaskManager()

    manager.create_task("TASK-006", "Pausar")

    manager.transition_task(
        "TASK-006",
        TaskState.PAUSED,
    )

    status = get_task_status(manager)

    assert status["paused_tasks"] == 1


def test_stopped_task_count():
    manager = TaskManager()

    manager.create_task("TASK-007", "Detener")

    manager.transition_task(
        "TASK-007",
        TaskState.STOPPED,
    )

    status = get_task_status(manager)

    assert status["stopped_tasks"] == 1


def test_error_task_count():
    manager = TaskManager()

    manager.create_task("TASK-008", "Error")

    manager.transition_task(
        "TASK-008",
        TaskState.ANALYZING,
    )
    manager.transition_task(
        "TASK-008",
        TaskState.ERROR,
    )

    status = get_task_status(manager)

    assert status["error_tasks"] == 1


def test_resource_limited_task_count():
    manager = TaskManager()

    manager.create_task("TASK-009", "Límite")

    manager.transition_task(
        "TASK-009",
        TaskState.ANALYZING,
    )
    manager.transition_task(
        "TASK-009",
        TaskState.WORKING,
    )
    manager.transition_task(
        "TASK-009",
        TaskState.RESOURCE_LIMIT,
    )

    status = get_task_status(manager)

    assert status["resource_limited_tasks"] == 1


def test_status_contains_state_breakdown():
    manager = TaskManager()

    manager.create_task("TASK-010", "Tarea")

    status = get_task_status(manager)

    assert "by_state" in status
    assert status["by_state"]["PENDING"] == 1
