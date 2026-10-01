import pytest

from src.supervisor.task import Task
from src.worker_5.task_executor import Worker5TaskExecutor


class MockHandler:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def execute(self, task):
        if self.error is not None:
            raise self.error
        return self.result


def create_assigned_task(task_id: str = "task-001") -> Task:
    task = Task(
        task_id=task_id,
        description="Worker 5 task",
    )
    task.assign("worker_5")
    return task


def test_executor_returns_handler_result():
    executor = Worker5TaskExecutor()
    task = create_assigned_task()
    handler = MockHandler(result="success")

    result = executor.execute(task, handler)

    assert result == "success"


def test_executor_completes_task_after_success():
    executor = Worker5TaskExecutor()
    task = create_assigned_task()
    handler = MockHandler(result="completed")

    executor.execute(task, handler)

    assert task.status == "completed"
    assert task.metadata["result"] == "completed"


def test_executor_starts_task_before_execution():
    executor = Worker5TaskExecutor()
    task = create_assigned_task()

    class StatusHandler:
        def execute(self, current_task):
            assert current_task.status == "running"
            return "ok"

    executor.execute(task, StatusHandler())

    assert task.status == "completed"


def test_executor_marks_task_failed_on_error():
    executor = Worker5TaskExecutor()
    task = create_assigned_task()
    handler = MockHandler(error=RuntimeError("execution failed"))

    with pytest.raises(RuntimeError, match="execution failed"):
        executor.execute(task, handler)

    assert task.status == "failed"
    assert task.metadata["error"] == "execution failed"


def test_executor_rejects_invalid_task():
    executor = Worker5TaskExecutor()
    handler = MockHandler(result="success")

    with pytest.raises(TypeError):
        executor.execute("invalid_task", handler)


def test_executor_rejects_task_for_another_worker():
    executor = Worker5TaskExecutor()
    task = Task(
        task_id="task-001",
        description="Wrong worker",
    )
    task.assign("worker_1")
    handler = MockHandler(result="success")

    with pytest.raises(ValueError):
        executor.execute(task, handler)


def test_executor_rejects_unassigned_task():
    executor = Worker5TaskExecutor()
    task = Task(
        task_id="task-001",
        description="Unassigned task",
    )
    handler = MockHandler(result="success")

    with pytest.raises(ValueError):
        executor.execute(task, handler)


def test_executor_rejects_missing_handler():
    executor = Worker5TaskExecutor()
    task = create_assigned_task()

    with pytest.raises(ValueError):
        executor.execute(task, None)


def test_executor_rejects_invalid_handler():
    executor = Worker5TaskExecutor()
    task = create_assigned_task()

    with pytest.raises(ValueError):
        executor.execute(task, object())


def test_executor_stores_successful_result():
    executor = Worker5TaskExecutor()
    task = create_assigned_task()
    handler = MockHandler(result={"output": "worker 5 completed"})

    result = executor.execute(task, handler)

    assert result == {"output": "worker 5 completed"}
    assert task.metadata["result"] == {"output": "worker 5 completed"}
