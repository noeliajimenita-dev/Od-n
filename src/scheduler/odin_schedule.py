from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Iterable


@dataclass(frozen=True)
class ScheduleWindow:
    start: time
    end: time

    def contains(self, current: time) -> bool:
        if self.start <= self.end:
            return self.start <= current <= self.end

        # Ventana que cruza medianoche.
        return current >= self.start or current <= self.end


@dataclass
class OdinSchedule:
    bot_id: str
    timezone: str = "America/Argentina/Buenos_Aires"
    weekday_windows: dict[int, list[ScheduleWindow]] = field(
        default_factory=dict
    )
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.bot_id or not self.bot_id.strip():
            raise ValueError("bot_id cannot be empty")

        if not self.timezone or not self.timezone.strip():
            raise ValueError("timezone cannot be empty")

        self._validate_weekdays()

    def _validate_weekdays(self) -> None:
        for weekday in self.weekday_windows:
            if weekday < 0 or weekday > 6:
                raise ValueError(
                    "weekday must be between 0 and 6"
                )

    def set_windows(
        self,
        weekday: int,
        windows: Iterable[ScheduleWindow],
    ) -> None:
        if weekday < 0 or weekday > 6:
            raise ValueError(
                "weekday must be between 0 and 6"
            )

        normalized = list(windows)

        if not normalized:
            raise ValueError(
                "At least one schedule window is required"
            )

        self.weekday_windows[weekday] = normalized

    def add_window(
        self,
        weekday: int,
        window: ScheduleWindow,
    ) -> None:
        if weekday < 0 or weekday > 6:
            raise ValueError(
                "weekday must be between 0 and 6"
            )

        self.weekday_windows.setdefault(
            weekday,
            [],
        ).append(window)

    def clear_windows(
        self,
        weekday: int,
    ) -> None:
        self.weekday_windows.pop(
            weekday,
            None,
        )

    def get_windows(
        self,
        weekday: int,
    ) -> list[ScheduleWindow]:
        return list(
            self.weekday_windows.get(
                weekday,
                [],
            )
        )

    def is_active(
        self,
        current_datetime: datetime,
    ) -> bool:
        if not self.enabled:
            return False

        windows = self.get_windows(
            current_datetime.weekday()
        )

        return any(
            window.contains(
                current_datetime.time()
            )
            for window in windows
        )

    def set_weekday_schedule(
        self,
        start: time = time(4, 0),
        end: time = time(22, 10),
        pause_start: time = time(13, 0),
        pause_end: time = time(14, 0),
    ) -> None:
        self.set_windows(
            0,
            self._work_windows(
                start,
                end,
                pause_start,
                pause_end,
            ),
        )
        self.set_windows(
            1,
            self._work_windows(
                start,
                end,
                pause_start,
                pause_end,
            ),
        )
        self.set_windows(
            2,
            self._work_windows(
                start,
                end,
                pause_start,
                pause_end,
            ),
        )
        self.set_windows(
            3,
            self._work_windows(
                start,
                end,
                pause_start,
                pause_end,
            ),
        )
        self.set_windows(
            4,
            self._work_windows(
                start,
                end,
                pause_start,
                pause_end,
            ),
        )

    def set_weekend_schedule(
        self,
        start: time = time(4, 0),
        end: time = time(20, 0),
        pause_start: time = time(13, 0),
        pause_end: time = time(14, 0),
    ) -> None:
        self.set_windows(
            5,
            self._work_windows(
                start,
                end,
                pause_start,
                pause_end,
            ),
        )
        self.set_windows(
            6,
            self._work_windows(
                start,
                end,
                pause_start,
                pause_end,
            ),
        )

    @staticmethod
    def _work_windows(
        start: time,
        end: time,
        pause_start: time,
        pause_end: time,
    ) -> list[ScheduleWindow]:
        if not (
            start < pause_start
            < pause_end
            < end
        ):
            raise ValueError(
                "Schedule must satisfy "
                "start < pause_start < pause_end < end"
            )

        return [
            ScheduleWindow(
                start=start,
                end=pause_start,
            ),
            ScheduleWindow(
                start=pause_end,
                end=end,
            ),
        ]

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def status(
        self,
        current_datetime: datetime,
    ) -> dict[str, object]:
        return {
            "bot_id": self.bot_id,
            "timezone": self.timezone,
            "enabled": self.enabled,
            "weekday": current_datetime.weekday(),
            "active": self.is_active(
                current_datetime
            ),
            "windows": [
                {
                    "start": window.start.isoformat(),
                    "end": window.end.isoformat(),
                }
                for window in self.get_windows(
                    current_datetime.weekday()
                )
            ],
      }
