"""
Estados y transiciones de tareas de THE ODIN PROJECT.
"""

from enum import Enum


class TaskState(str, Enum):
    """Estados posibles de una tarea."""

    PENDING = "PENDING"
    ANALYZING = "ANALYZING"
    PROPOSING = "PROPOSING"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    WORKING = "WORKING"
    TESTING = "TESTING"
    WAITING_USER = "WAITING_USER"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"
    RESOURCE_LIMIT = "RESOURCE_LIMIT"
    ERROR = "ERROR"
    STOPPED = "STOPPED"


ALLOWED_TRANSITIONS = {
    TaskState.PENDING: {
        TaskState.ANALYZING,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.ANALYZING: {
        TaskState.PROPOSING,
        TaskState.WORKING,
        TaskState.ERROR,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.PROPOSING: {
        TaskState.WAITING_APPROVAL,
        TaskState.WORKING,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.WAITING_APPROVAL: {
        TaskState.WORKING,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.WORKING: {
        TaskState.TESTING,
        TaskState.WAITING_USER,
        TaskState.RESOURCE_LIMIT,
        TaskState.ERROR,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.TESTING: {
        TaskState.WORKING,
        TaskState.COMPLETED,
        TaskState.ERROR,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.WAITING_USER: {
        TaskState.WORKING,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.RESOURCE_LIMIT: {
        TaskState.WAITING_USER,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.PAUSED: {
        TaskState.WORKING,
        TaskState.WAITING_USER,
        TaskState.STOPPED,
    },
    TaskState.ERROR: {
        TaskState.WORKING,
        TaskState.PAUSED,
        TaskState.STOPPED,
    },
    TaskState.COMPLETED: set(),
    TaskState.STOPPED: set(),
}


def can_transition(
    current: TaskState,
    target: TaskState,
) -> bool:
    """Comprueba si una transición de estado está permitida."""

    return target in ALLOWED_TRANSITIONS.get(
        current,
        set(),
)
