import pytest

from src.supervisor.task_analyzer import TaskAnalyzer


def test_analyzer_creates_task():
    analyzer = TaskAnalyzer()

    task = analyzer.analyze(
        task_id="task-001",
        instruction="  Analyze   client   request  ",
        priority=2,
    )

    assert task.task_id == "task-001"
    assert task.description == "Analyze client request"
    assert task.priority == 2
    assert task.status == "pending"
    assert task.metadata["source"] == "supervisor"
    assert task.metadata["analyzed"] is True


def test_analyzer_rejects_empty_instruction():
    analyzer = TaskAnalyzer()

    with pytest.raises(ValueError, match="Task instruction cannot be empty"):
        analyzer.analyze(
            task_id="task-001",
            instruction="   ",
        )


def test_analyzer_uses_default_priority():
    analyzer = TaskAnalyzer()

    task = analyzer.analyze(
        task_id="task-002",
        instruction="Run quality check",
    )

    assert task.priority == 0
