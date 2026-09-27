"""
Estado general del Task Manager de THE ODIN PROJECT.
"""

from collections import Counter

from .manager import TaskManager
from .states import TaskState


def get_task_status(manager: TaskManager) -> dict:
    """Devuelve un resumen del estado de las tareas."""

    tasks = manager.get_all_tasks()

    state_counts = Counter(
        task.state.value
        for task in tasks
    )

    active_states = {
        TaskState.ANALYZING,
        TaskState.PROPOSING,
        TaskState.WAITING_APPROVAL,
        TaskState.WORKING,
        TaskState.TESTING,
        TaskState.WAITING_USER,
    }

    active_tasks = [
        task.task_id
        for task in tasks
        if task.state in active_states
    ]

    return {
        "total_tasks": len(tasks),
        "active_tasks": len(active_tasks),
        "active_task_ids": active_tasks,
        "completed_tasks": state_counts.get(
            TaskState.COMPLETED.value,
            0,
        ),
        "paused_tasks": state_counts.get(
            TaskState.PAUSED.value,
            0,
        ),
        "stopped_tasks": state_counts.get(
            TaskState.STOPPED.value,
            0,
        ),
        "error_tasks": state_counts.get(
            TaskState.ERROR.value,
            0,
        ),
        "resource_limited_tasks": state_counts.get(
            TaskState.RESOURCE_LIMIT.value,
            0,
        ),
        "by_state": dict(state_counts),
    }
