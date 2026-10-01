import pytest

from src.supervisor.task import Task
from src.supervisor.task_assignment_monitor import TaskAssignmentMonitor


def create_task(task_id: str, status: str) -> Task:
    task = Task(
        task_id=task_id,
        description=f"Task {task_id}",
    )
    task.status = status
    return task


def test_monitor_returns_empty_status():
    monitor = TaskAssignmentMonitor()

    result = monitor.get_status({})

    assert result == {
        "total": 0,
        "assigned": [],
        "running": [],
        "completed": [],
        "failed": [],
        "pending": [],
    }


def test_monitor_classifies_task_statuses():
    monitor = TaskAssignmentMonitor()

    tasks = {
        "task-001": create_task("task-001", "pending"),
        "task-002": create_task("task-002", "assigned"),
        "task-003": create_task("task-003", "running"),
        "task-004": create_task("task-004", "completed"),
        "task-005": create_task("task-005", "failed"),
    }

    result = monitor.get_status(tasks)

    assert result["total"] == 5
    assert result["pending"] == ["task-001"]
    assert result["assigned"] == ["task-002"]
    assert result["running"] == ["task-003"]
    assert result["completed"] == ["task-004"]
    assert result["failed"] == ["task-005"]


def test_monitor_returns_active_tasks():
    monitor = TaskAssignmentMonitor()

    tasks = {
        "task-001": create_task("task-001", "assigned"),
        "task-002": create_task("task-002", "running"),
        "task-003": create_task("task-003", "completed"),
    }

    assert monitor.active_tasks(tasks) == [
        "task-001",
        "task-002",
    ]


def test_monitor_returns_completed_tasks():
    monitor = TaskAssignmentMonitor()

    tasks = {
        "task-001": create_task("task-001", "completed"),
        "task-002": create_task("task-002", "running"),
        "task-003": create_task("task-003", "completed"),
    }

    assert monitor.completed_tasks(tasks) == [
        "task-001",
        "task-003",
    ]


def test_monitor_returns_failed_tasks():
    monitor = TaskAssignmentMonitor()

    tasks = {
        "task-001": create_task("task-001", "failed"),
        "task-002": create_task("task-002", "completed"),
        "task-003": create_task("task-003", "failed"),
    }

    assert monitor.failed_tasks(tasks) == [
        "task-001",
        "task-003",
    ]


def test_monitor_detects_active_tasks():
    monitor = TaskAssignmentMonitor()

    tasks = {
        "task-001": create_task("task-001", "assigned"),
    }

    assert monitor.has_active_tasks(tasks) is True


def test_monitor_detects_no_active_tasks():
    monitor = TaskAssignmentMonitor()

    tasks = {
        "task-001": create_task("task-001", "completed"),
        "task-002": create_task("task-002", "failed"),
    }

    assert monitor.has_active_tasks(tasks) is False


def test_monitor_handles_unknown_status():
    monitor = TaskAssignmentMonitor()

    task = create_task("task-001", "unknown")

    result = monitor.get_status({"task-001": task})

    assert result["total"] == 1
    assert result["assigned"] == []
    assert result["running"] == []
    assert result["completed"] == []
    assert result["failed"] == []
    assert result["pending"] == []


def test_monitor_does_not_modify_tasks():
    monitor = TaskAssignmentMonitor()

    task = create_task("task-001", "assigned")
    tasks = {"task-001": task}

    monitor.get_status(tasks)

    assert task.status == "assigned"
    assert tasks["task-001"] is task
