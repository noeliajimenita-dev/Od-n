import pytest

from src.supervisor.task import Task
from src.worker_3.task_receiver import Worker3TaskReceiver


def create_assigned_task(task_id: str) -> Task:
    task = Task(
        task_id=task_id,
        description=f"Task {task_id}",
    )
    task.assign("worker_3")
    return task


def test_receiver_starts_empty():
    receiver = Worker3TaskReceiver()

    assert receiver.has_pending_tasks() is False
    assert receiver.next_task() is None


def test_receiver_accepts_assigned_worker_3_task():
    receiver = Worker3TaskReceiver()
    task = create_assigned_task("task-001")

    result = receiver.receive(task)

    assert result is task
    assert receiver.has_pending_tasks() is True


def test_receiver_returns_next_task():
    receiver = Worker3TaskReceiver()
    task = create_assigned_task("task-001")

    receiver.receive(task)

    result = receiver.next_task()

    assert result is task
    assert receiver.has_pending_tasks() is False


def test_receiver_processes_tasks_in_order():
    receiver = Worker3TaskReceiver()

    first = create_assigned_task("task-001")
    second = create_assigned_task("task-002")

    receiver.receive(first)
    receiver.receive(second)

    assert receiver.next_task() is first
    assert receiver.next_task() is second
    assert receiver.next_task() is None


def test_receiver_rejects_invalid_object():
    receiver = Worker3TaskReceiver()

    with pytest.raises(TypeError):
        receiver.receive("invalid_task")


def test_receiver_rejects_unassigned_task():
    receiver = Worker3TaskReceiver()
    task = Task(
        task_id="task-001",
        description="Unassigned task",
    )

    with pytest.raises(ValueError):
        receiver.receive(task)


def test_receiver_rejects_task_for_another_worker():
    receiver = Worker3TaskReceiver()

    task = Task(
        task_id="task-001",
        description="Wrong worker",
    )
    task.assign("worker_1")

    with pytest.raises(ValueError):
        receiver.receive(task)


def test_has_pending_tasks_changes_after_retrieval():
    receiver = Worker3TaskReceiver()
    task = create_assigned_task("task-001")

    receiver.receive(task)

    assert receiver.has_pending_tasks() is True

    receiver.next_task()

    assert receiver.has_pending_tasks() is False
