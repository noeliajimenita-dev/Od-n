import pytest

from src.supervisor.task import Task
from src.worker_4.worker import Worker4


def test_worker_has_default_identity():
    worker = Worker4()

    assert worker.worker_id == "worker_4"
    assert worker.status == "idle"
    assert worker.current_task is None


def test_worker_can_handle_skill():
    worker = Worker4(skills=["data_analysis"])

    assert worker.can_handle("data_analysis") is True
    assert worker.can_handle("cybersecurity") is False


def test_worker_accepts_task_when_idle():
    worker = Worker4()
    task = Task(
        task_id="task-001",
        description="Analyze dataset",
    )

    worker.accept_task(task)

    assert worker.current_task is task
    assert worker.status == "working"


def test_worker_rejects_invalid_task():
    worker = Worker4()

    with pytest.raises(TypeError):
        worker.accept_task("invalid_task")


def test_worker_cannot_accept_task_while_working():
    worker = Worker4()

    first_task = Task(
        task_id="task-001",
        description="First task",
    )
    second_task = Task(
        task_id="task-002",
        description="Second task",
    )

    worker.accept_task(first_task)

    with pytest.raises(RuntimeError):
        worker.accept_task(second_task)


def test_worker_completes_task_and_returns_to_idle():
    worker = Worker4()
    task = Task(
        task_id="task-001",
        description="Complete task",
    )

    worker.accept_task(task)

    completed_task = worker.complete_task()

    assert completed_task is task
    assert worker.current_task is None
    assert worker.status == "idle"


def test_worker_cannot_complete_without_active_task():
    worker = Worker4()

    with pytest.raises(RuntimeError):
        worker.complete_task()


def test_worker_can_pause_when_idle():
    worker = Worker4()

    worker.pause()

    assert worker.status == "paused"


def test_worker_can_resume_from_paused():
    worker = Worker4()

    worker.pause()
    worker.resume()

    assert worker.status == "idle"


def test_worker_cannot_pause_with_active_task():
    worker = Worker4()
    task = Task(
        task_id="task-001",
        description="Active task",
    )

    worker.accept_task(task)

    with pytest.raises(RuntimeError):
        worker.pause()
