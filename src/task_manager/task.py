"""
Modelo de tareas de THE ODIN PROJECT.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .states import TaskState


def utc_now() -> datetime:
    """Devuelve la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Task:
    """Representa una tarea administrada por THE ODIN PROJECT."""

    task_id: str
    description: str
    state: TaskState = TaskState.PENDING
    priority: int = 5
    assigned_to: str | None = None

    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    result: Any = None
    error: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def update_state(self, new_state: TaskState) -> None:
        """Actualiza el estado y la fecha de modificación."""
        self.state = new_state
        self.updated_at = utc_now()

    def assign(self, worker: str) -> None:
        """Asigna la tarea a un bot o componente."""
        if not worker:
            raise ValueError("El responsable no puede estar vacío.")

        self.assigned_to = worker
        self.updated_at = utc_now()

    def set_result(self, result: Any) -> None:
        """Guarda el resultado de la tarea."""
        self.result = result
        self.error = None
        self.updated_at = utc_now()

    def set_error(self, error: str) -> None:
        """Registra un error asociado a la tarea."""
        if not error:
            raise ValueError("El error no puede estar vacío.")

        self.error = error
        self.updated_at = utc_now()

    def is_finished(self) -> bool:
        """Indica si la tarea terminó definitivamente."""
        return self.state in {
            TaskState.COMPLETED,
            TaskState.STOPPED,
        }

    def to_dict(self) -> dict[str, Any]:
        """Convierte la tarea a un diccionario serializable."""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "state": self.state.value,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "result": self.result,
            "error": self.error,
            "metadata": self.metadata.copy(),
      }
