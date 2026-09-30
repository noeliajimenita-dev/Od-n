import pytest

from src.supervisor.task import Task
from src.supervisor.task_executor import TaskExecutor


class FakeBot:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def execute(self, task):
        if self.error:
            raise RuntimeError(self.error)

        return self.result


def create_assigned_task():
    task = Task(
        task_id="task-001",
        description="Execute client work",
    )
    task.assign("bot_1")
    return task


def test_executor_runs_assigned_task():
    task = create_assigned_task()

    executor = TaskExecutor(
        bot_handlers={
            "bot_1": FakeBot(result="Work completed"),
        }
    )

    result = executor.execute(task)

    assert result == "Work completed"
    assert task.status == "completed"
    assert task.metadata["result"] == "Work completed"


def test_executor_marks_task_as_failed():
    task = create_assigned_task()

    executor = TaskExecutor(
        bot_handlers={
            "bot_1": FakeBot(error="Execution failed"),
        }
    )

    with pytest.raises(RuntimeError, match="Execution failed"):
        executor.execute(task)

    assert task.status == "failed"
    assert task.metadata["error"] == "Execution failed"


def test_executor_rejects_unassigned_task():
    task = Task(
        task_id="task-002",
        description="Execute client work",
    )

    executor = TaskExecutor(
        bot_handlers={
            "bot_1": FakeBot(result="Work completed"),
        }
    )

    with pytest.raises(ValueError, match="Task has no assigned bot"):
        executor.execute(task)


def test_executor_rejects_missing_bot_handler():
    task = create_assigned_task()

    executor = TaskExecutor(
        bot_handlers={}
    )

    with pytest.raises(
        ValueError,
        match="No handler available for bot",
    ):
        executor.execute(task)
