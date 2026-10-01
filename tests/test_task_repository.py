import pytest

from src.supervisor.task import Task
from src.supervisor.task_repository import TaskRepository


def build_task(task_id="task-1"):
    return Task(
        task_id=task_id,
        description="Test task",
    )


def test_repository_starts_empty():
    repository = TaskRepository()

    assert repository.count() == 0
    assert repository.list_tasks() == []


def test_repository_saves_task():
    repository = TaskRepository()
    task = build_task()

    saved = repository.save(task)

    assert saved is task
    assert repository.count() == 1


def test_repository_gets_task():
    repository = TaskRepository()
    task = build_task()

    repository.save(task)

    result = repository.get("task-1")

    assert result is task


def test_repository_returns_none_for_missing_task():
    repository = TaskRepository()

    assert repository.get("missing") is None


def test_repository_checks_task_existence():
    repository = TaskRepository()
    task = build_task()

    assert repository.exists("task-1") is False

    repository.save(task)

    assert repository.exists("task-1") is True


def test_repository_deletes_task():
    repository = TaskRepository()
    task = build_task()

    repository.save(task)

    assert repository.delete("task-1") is True
    assert repository.exists("task-1") is False
    assert repository.count() == 0


def test_repository_delete_missing_task_returns_false():
    repository = TaskRepository()

    assert repository.delete("missing") is False


def test_repository_lists_tasks():
    repository = TaskRepository()

    first = build_task("task-1")
    second = build_task("task-2")

    repository.save(first)
    repository.save(second)

    tasks = repository.list_tasks()

    assert tasks == [first, second]


def test_repository_replaces_task_with_same_id():
    repository = TaskRepository()

    first = build_task("task-1")
    second = build_task("task-1")

    repository.save(first)
    repository.save(second)

    assert repository.count() == 1
    assert repository.get("task-1") is second


def test_repository_clear_removes_all_tasks():
    repository = TaskRepository()

    repository.save(build_task("task-1"))
    repository.save(build_task("task-2"))

    repository.clear()

    assert repository.count() == 0
    assert repository.list_tasks() == []


def test_repository_rejects_invalid_task():
    repository = TaskRepository()

    with pytest.raises(TypeError):
        repository.save("invalid-task")


def test_repository_rejects_empty_task_id():
    repository = TaskRepository()

    task = build_task("")
    
    with pytest.raises(ValueError):
        repository.save(task)


def test_repository_normalizes_task_id_on_get():
    repository = TaskRepository()
    task = build_task("task-1")

    repository.save(task)

    assert repository.get("  task-1  ") is task


def test_repository_normalizes_task_id_on_delete():
    repository = TaskRepository()
    task = build_task("task-1")

    repository.save(task)

    assert repository.delete("  task-1  ") is True
    assert repository.exists("task-1") is False
