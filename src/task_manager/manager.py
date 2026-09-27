"""
Gestor de tareas de THE ODIN PROJECT.
"""

from .states import TaskState, can_transition
from .task import Task


class TaskManager:
    """Gestiona el ciclo de vida de las tareas."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def create_task(
        self,
        task_id: str,
        description: str,
        priority: int = 5,
    ) -> Task:
        """Crea y registra una nueva tarea."""
        if not task_id:
            raise ValueError("El task_id no puede estar vacío.")

        if not description:
            raise ValueError("La descripción no puede estar vacía.")

        if task_id in self._tasks:
            raise ValueError(f"La tarea ya existe: {task_id}")

        if priority < 1:
            raise ValueError("La prioridad debe ser mayor o igual a 1.")

        task = Task(
            task_id=task_id,
            description=description,
            priority=priority,
        )

        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Task | None:
        """Obtiene una tarea por su identificador."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Devuelve todas las tareas registradas."""
        return list(self._tasks.values())

    def assign_task(self, task_id: str, worker: str) -> Task:
        """Asigna una tarea a un worker."""
        task = self._require_task(task_id)
        task.assign(worker)
        return task

    def transition_task(
        self,
        task_id: str,
        new_state: TaskState,
    ) -> Task:
        """Cambia el estado si la transición está permitida."""
        task = self._require_task(task_id)

        if not can_transition(task.state, new_state):
            raise ValueError(
                f"Transición no permitida: "
                f"{task.state.value} -> {new_state.value}"
            )

        task.update_state(new_state)
        return task

    def set_result(self, task_id: str, result) -> Task:
        """Guarda el resultado de una tarea."""
        task = self._require_task(task_id)
        task.set_result(result)
        return task

    def set_error(self, task_id: str, error: str) -> Task:
        """Registra un error en una tarea."""
        task = self._require_task(task_id)
        task.set_error(error)
        return task

    def remove_task(self, task_id: str) -> bool:
        """Elimina una tarea del gestor."""
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True

    def count(self) -> int:
        """Devuelve la cantidad de tareas registradas."""
        return len(self._tasks)

    def _require_task(self, task_id: str) -> Task:
        """Obtiene una tarea o genera un error si no existe."""
        task = self.get_task(task_id)

        if task is None:
            raise KeyError(f"Tarea no encontrada: {task_id}")

        return task
