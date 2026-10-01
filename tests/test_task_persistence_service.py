import pytest

from src.supervisor.task import Task
from src.supervisor.task_persistence_service import TaskPersistenceService
from src.supervisor.task_repository import TaskRepository


def build_service():
    return TaskPersistenceService(TaskRepository())


def build_task(task_id="task-1", description="Test task"):
    return Task(
        task_id=task_id,
        description=description,
    )


def test_service_requires_repository():
    with pytest.raises(ValueError):
        TaskPersistenceService(None)


def test_service_saves_task():
    service = build_service()
    task = build_task()

    result = service.save(task)

    assert result is task
    assert service.count() == 1


def test_service_gets_task():
    service = build_service()
    task = build_task()

    service.save(task)

    assert service.get("task-1") is task


def test_service_checks_existence():
    service = build_service()
    task = build_task()

    assert service.exists("task-1") is False

    service.save(task)

    assert service.exists("task-1") is True


def test_service_updates_existing_task():
    service = build_service()

    original = build_task(description="Original")
    service.save(original)

    updated = build_task(description="Updated")
    result = service.update(updated)

    assert result is updated
    assert service.get("task-1").description == "Updated"
    assert service.count() == 1


def test_service_rejects_update_for_missing_task():
    service = build_service()

    with pytest.raises(ValueError):
        service.update(build_task("missing"))


def test_service_deletes_task():
    service = build_service()
    service.save(build_task())

    assert service.delete("task-1") is True
    assert service.exists("task-1") is False


def test_service_lists_tasks():
    service = build_service()

    first = build_task("task-1")
    second = build_task("task-2")

    service.save(first)
    service.save(second)

    assert service.list_tasks() == [first, second]


def test_service_counts_tasks():
    service = build_service()

    service.save(build_task("task-1"))
    service.save(build_task("task-2"))

    assert service.count() == 2


def test_service_clears_tasks():
    service = build_service()

    service.save(build_task("task-1"))
    service.save(build_task("task-2"))

    service.clear()

    assert service.count() == 0
    assert service.list_tasks() == []


def test_service_rejects_invalid_task():
    service = build_service()

    with pytest.raises(TypeError):
        service.save("invalid-task")


def test_service_rejects_invalid_task_on_update():
    service = build_service()

    with pytest.raises(TypeError):
        service.update("invalid-task")
