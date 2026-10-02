from __future__ import annotations

from datetime import datetime
from typing import Any

from .odin_schedule import OdinSchedule
from .odin_log_service import OdinLogService
from .odin_scheduler import OdinScheduler


class OdinRuntimeManager:
    """
    Control central del runtime de ODIN.

    Coordina:
    - Scheduler.
    - Horarios individuales.
    - Estado global del runtime.
    - Logs operativos.
    """

    VALID_STATES = {
        "stopped",
        "running",
        "paused",
    }

    def __init__(
        self,
        scheduler: OdinScheduler | None = None,
        log_service: OdinLogService | None = None,
    ) -> None:
        self.scheduler = scheduler or OdinScheduler()
        self.log_service = (
            log_service or OdinLogService()
        )

        self._state = "stopped"
        self._schedules: dict[str, OdinSchedule] = {}

    def register_bot(
        self,
        schedule: OdinSchedule,
    ) -> None:
        if not isinstance(
            schedule,
            OdinSchedule,
        ):
            raise TypeError(
                "schedule must be an OdinSchedule"
            )

        self._schedules[schedule.bot_id] = schedule

        for weekday, windows in (
            schedule.weekday_windows.items()
        ):
            self.scheduler.set_schedule(
                bot_id=schedule.bot_id,
                weekday=weekday,
                windows=windows,
            )

    def start(self) -> None:
        if self._state == "running":
            return

        self._state = "running"

    def pause(self) -> None:
        if self._state == "stopped":
            raise RuntimeError(
                "Runtime is stopped"
            )

        self._state = "paused"

    def resume(self) -> None:
        if self._state == "stopped":
            raise RuntimeError(
                "Runtime is stopped"
            )

        self._state = "running"

    def stop(self) -> None:
        self._state = "stopped"

    def is_running(self) -> bool:
        return self._state == "running"

    def is_paused(self) -> bool:
        return self._state == "paused"

    def is_stopped(self) -> bool:
        return self._state == "stopped"

    def bot_should_work(
        self,
        bot_id: str,
        current_datetime: datetime | None = None,
    ) -> bool:
        if self._state != "running":
            return False

        schedule = self._schedules.get(bot_id)

        if schedule is None:
            return False

        current = (
            current_datetime
            or datetime.now()
        )

        return schedule.is_active(current)

    def run_once(
        self,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = (
            current_datetime
            or datetime.now()
        )

        if self._state != "running":
            return {
                "status": self._state,
                "executed": {},
            }

        results = self.scheduler.run_ready_tasks(
            current
        )

        for bot_id in self._schedules:
            if self.bot_should_work(
                bot_id,
                current,
            ):
                self.log_service.set_status(
                    bot_id,
                    "working",
                )
            else:
                self.log_service.set_status(
                    bot_id,
                    "paused",
                )

        return {
            "status": self._state,
            "timestamp": current.isoformat(),
            "executed": results,
        }

    def get_bot_status(
        self,
        bot_id: str,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = (
            current_datetime
            or datetime.now()
        )

        schedule = self._schedules.get(bot_id)

        if schedule is None:
            return {
                "bot_id": bot_id,
                "registered": False,
                "should_work": False,
            }

        should_work = self.bot_should_work(
            bot_id,
            current,
        )

        log = self.log_service.get_today(
            bot_id
        )

        return {
            "bot_id": bot_id,
            "registered": True,
            "runtime_state": self._state,
            "should_work": should_work,
            "schedule_enabled": schedule.enabled,
            "daily_log": log.summary(),
        }

    def status(
        self,
        current_datetime: datetime | None = None,
    ) -> dict[str, Any]:
        current = (
            current_datetime
            or datetime.now()
        )

        bots = {
            bot_id: self.get_bot_status(
                bot_id,
                current,
            )
            for bot_id in self._schedules
        }

        return {
            "runtime_state": self._state,
            "timestamp": current.isoformat(),
            "bots": bots,
            "scheduler": self.scheduler.status(
                current
            ),
            "daily_summary": self.log_service.summary(),
        }

    def list_bots(self) -> list[str]:
        return list(self._schedules.keys())

    def remove_bot(
        self,
        bot_id: str,
    ) -> None:
        self._schedules.pop(
            bot_id,
            None,
        )

        self.scheduler.remove_bot_schedule(
            bot_id
      )
