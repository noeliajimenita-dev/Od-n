import pytest

from src.supervisor.task import Task
from src.worker_2.task_receiver import Worker2TaskReceiver


def create_assigned_task(
    task_id: str = "task-001",
) -> Task:
    task = Task(
        task_id=task_id,
        description="Test task",
    )
    task.assign("worker_2")
    return task


def test_receiver_starts_empty():
    receiver = Worker2TaskReceiver()

    assert receiver.has_pending_tasks() is False
    assert receiver.next_task() is None


def test_receiver_accepts_worker_2_task():
    receiver = Worker2TaskReceiver()
    task = create_assigned_task()

    result = receiver.receive(task)

    assert result is task
    assert receiver.has_pending_tasks() is True


def test_receiver_returns_tasks_in_order():
    receiver = Worker2TaskReceiver()

    first = create_assigned_task("task-001")
    second = create_assigned_task("task-002")

    receiver.receive(first)
    receiver.receive(second)

    assert receiver.next_task() is first
    assert receiver.next_task() is second


def test_receiver_becomes_empty_after_all_tasks_are_taken():
    receiver = Worker2TaskReceiver()
    task = create_assigned_task()

    receiver.receive(task)
    receiver.next_task()

    assert receiver.has_pending_tasks() is False
    assert receiver.next_task() is None


def test_receiver_rejects_invalid_task_type():
    receiver = Worker2TaskReceiver()

    with pytest.raises(TypeError):
        receiver.receive("invalid_task")


def test_receiver_rejects_unassigned_task():
    receiver = Worker2TaskReceiver()

    task = Task(
        task_id="task-001",
        description="Unassigned task",
    )

    with pytest.raises(ValueError):
        receiver.receive(task)


def test_receiver_rejects_task_for_another_worker():
    receiver = Worker2TaskReceiver()

    task = Task(
        task_id="task-001",
        description="Other worker task",
    )
    task.assign("worker_1")

    with pytest.raises(ValueError):
        receiver.receive(task)


def test_receiver_accepts_multiple_tasks():
    receiver = Worker2TaskReceiver()

    tasks = [
        create_assigned_task("task-001"),
        create_assigned_task("task-002"),
        create_assigned_task("task-003"),
    ]

    for task in tasks:
        receiver.receive(task)

    assert receiver.has_pending_tasks() is True
    assert receiver.next_task() is tasks[0]
    assert receiver.next_task() is tasks[1]
    assert receiver.next_task() is tasks[2]
    assert receiver.next_task() is None
