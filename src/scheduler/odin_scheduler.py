from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Callable, Any


@dataclass
class ScheduleWindow:
    start: time
    end: time

    def contains(self, current_time: time) -> bool:
        if self.start <= self.end:
            return self.start <= current_time <= self.end

        # Permite ventanas que atraviesan medianoche.
        return current_time >= self.start or current_time <= self.end


@dataclass
class ScheduledTask:
    task_id: str
    bot_id: str
    callback: Callable[[], Any]
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class OdinScheduler:
    """
    Scheduler central de ODIN.

    Responsabilidades:
    - Registrar horarios por bot.
    - Registrar tareas programadas.
    - Determinar si un bot debe trabajar ahora.
    - Ejecutar tareas habilitadas cuando corresponde.
    - Pausar la ejecución fuera de las ventanas configuradas.
    """

    DEFAULT_WEEKDAY_WINDOW = ScheduleWindow(
        start=time(4, 0),
        end=time(22, 10),
    )

    DEFAULT_WEEKEND_WINDOW = ScheduleWindow(
        start=time(4, 0),
        end=time(20, 0),
    )

    def __init__(self) -> None:
        self._schedules: dict[str, dict[int, list[ScheduleWindow]]] = {}
        self._tasks: dict[str, ScheduledTask] = {}

    def set_schedule(
        self,
        bot_id: str,
        weekday: int,
        windows: list[ScheduleWindow],
    ) -> None:
        if not bot_id or not bot_id.strip():
            raise ValueError("bot_id cannot be empty")

        if weekday < 0 or weekday > 6:
            raise ValueError("weekday must be between 0 and 6")

        if not windows:
            raise ValueError("At least one schedule window is required")

        self._schedules.setdefault(bot_id, {})[
            weekday
        ] = list(windows)

    def get_schedule(
        self,
        bot_id: str,
        weekday: int,
    ) -> list[ScheduleWindow]:
        return list(
            self._schedules.get(bot_id, {}).get(
                weekday,
                [],
            )
        )

    def is_working(
        self,
        bot_id: str,
        current_datetime: datetime | None = None,
    ) -> bool:
        if not bot_id:
            return False

        current = current_datetime or datetime.now()
        weekday = current.weekday()

        windows = self.get_schedule(
            bot_id,
            weekday,
        )

        return any(
            window.contains(current.time())
            for window in windows
        )

    def set_default_schedule(
        self,
        bot_id: str,
    ) -> None:
        self.set_schedule(
            bot_id=bot_id,
            weekday=0,
            windows=[self.DEFAULT_WEEKDAY_WINDOW],
        )
        self.set_schedule(
            bot_id=bot_id,
            weekday=1,
            windows=[self.DEFAULT_WEEKDAY_WINDOW],
        )
        self.set_schedule(
            bot_id=bot_id,
            weekday=2,
            windows=[self.DEFAULT_WEEKDAY_WINDOW],
        )
        self.set_schedule(
            bot_id=bot_id,
            weekday=3,
            windows=[self.DEFAULT_WEEKDAY_WINDOW],
        )
        self.set_schedule(
            bot_id=bot_id,
            weekday=4,
            windows=[self.DEFAULT_WEEKDAY_WINDOW],
        )

        self.set_schedule(
            bot_id=bot_id,
            weekday=5,
            windows=[self.DEFAULT_WEEKEND_WINDOW],
        )
        self.set_schedule(
            bot_id=bot_id,
            weekday=6,
            windows=[self.DEFAULT_WEEKEND_WINDOW],
        )

    def register_task(
        self,
        task: ScheduledTask,
    ) -> None:
        if not task.task_id:
            raise ValueError("task_id cannot be empty")

        if not task.bot_id:
            raise ValueError("bot_id cannot be empty")

        self._tasks[task.task_id] = task

    def enable_task(
        self,
        task_id: str,
    ) -> None:
        task = self._require_task(task_id)
        task.enabled = True

    def disable_task(
        self,
        task_id: str,
    ) -> None:
        task = self._require_task(task_id)
        task.enabled = False

    def run_ready_tasks(
        self,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = current_datetime or datetime.now()
        results: dict[str, Any] = {}

        for task_id, task in self._tasks.items():
            if not task.enabled:
                continue

            if not self.is_working(
                task.bot_id,
                current,
            ):
                continue

            try:
                results[task_id] = task.callback()
            except Exception as exc:
                results[task_id] = {
                    "status": "error",
                    "error": str(exc),
                }

        return results

    def list_tasks(self) -> list[ScheduledTask]:
        return list(self._tasks.values())

    def status(
        self,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = current_datetime or datetime.now()

        working_bots = [
            bot_id
            for bot_id in self._schedules
            if self.is_working(
                bot_id,
                current,
            )
        ]

        enabled_tasks = [
            task_id
            for task_id, task in self._tasks.items()
            if task.enabled
        ]

        return {
            "current_time": current.isoformat(),
            "working_bots": working_bots,
            "registered_bots": list(
                self._schedules.keys()
            ),
            "total_tasks": len(self._tasks),
            "enabled_tasks": enabled_tasks,
        }

    def remove_task(
        self,
        task_id: str,
    ) -> None:
        self._tasks.pop(
            task_id,
            None,
        )

    def remove_bot_schedule(
        self,
        bot_id: str,
    ) -> None:
        self._schedules.pop(
            bot_id,
            None,
        )

    def _require_task(
        self,
        task_id: str,
    ) -> ScheduledTask:
        task = self._tasks.get(task_id)

        if task is None:
            raise KeyError(
                f"Scheduled task not found: {task_id}"
            )

        return task
