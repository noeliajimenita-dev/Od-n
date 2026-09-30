import pytest

from src.supervisor.task import Task
from src.supervisor.task_dispatcher import TaskDispatcher


def test_dispatcher_assigns_selected_bot():
    dispatcher = TaskDispatcher(
        available_bots=["bot_1", "bot_2", "bot_3"]
    )

    task = Task(
        task_id="task-001",
        description="Analyze client request",
    )

    result = dispatcher.dispatch(task, bot_name="bot_2")

    assert result.bot_name == "bot_2"
    assert result.status == "assigned"


def test_dispatcher_selects_available_bot():
    dispatcher = TaskDispatcher(
        available_bots=["bot_1", "bot_2"]
    )

    task = Task(
        task_id="task-002",
        description="Run quality check",
    )

    result = dispatcher.dispatch(task)

    assert result.bot_name == "bot_1"
    assert result.status == "assigned"


def test_dispatcher_rejects_unavailable_bot():
    dispatcher = TaskDispatcher(
        available_bots=["bot_1", "bot_2"]
    )

    task = Task(
        task_id="task-003",
        description="Process data",
    )

    with pytest.raises(ValueError, match="Bot not available"):
        dispatcher.dispatch(task, bot_name="bot_5")


def test_dispatcher_rejects_when_no_bots_are_available():
    dispatcher = TaskDispatcher()

    task = Task(
        task_id="task-004",
        description="Process data",
    )

    with pytest.raises(ValueError, match="No available bot"):
        dispatcher.dispatch(task)
