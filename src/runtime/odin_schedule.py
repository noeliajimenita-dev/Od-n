"""
Odin Schedule module for managing execution schedules, pauses, and activation states.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
import datetime


@dataclass
class ScheduleConfig:
    """Configuration for schedule timing and intervals."""
    interval_seconds: int = 60
    enabled_by_default: bool = True


class OdinSchedule:
    """Manages the schedule, activation state, and pauses for Odin runtime tasks."""

    def __init__(self, config: Optional[ScheduleConfig] = None) -> None:
        self.config = config or ScheduleConfig()
        self._active: bool = self.config.enabled_by_default
        self._paused: bool = False
        self._last_execution: Optional[datetime.datetime] = None
        self._pause_reason: Optional[str] = None

    def is_active(self) -> bool:
        """Returns whether the schedule is currently active."""
        return self._active

    def activate(self) -> None:
        """Activates the schedule."""
        self._active = True

    def deactivate(self) -> None:
        """Deactivates the schedule."""
        self._active = False

    def is_paused(self) -> bool:
        """Returns whether the schedule is currently paused."""
        return self._paused

    def pause(self, reason: Optional[str] = None) -> None:
        """Pauses the schedule execution."""
        self._paused = True
        self._pause_reason = reason

    def resume(self) -> None:
        """Resumes the schedule execution."""
        self._paused = False
        self._pause_reason = None

    def can_execute(self) -> bool:
        """Determines if a scheduled task can run based on active and pause states."""
        return self._active and not self._paused

    def record_execution(self) -> None:
        """Records the timestamp of the last execution."""
        self._last_execution = datetime.datetime.now(datetime.timezone.utc)

    def get_status(self) -> Dict[str, Any]:
        """Returns a status dictionary of the schedule."""
        return {
            "active": self._active,
            "paused": self._paused,
            "pause_reason": self._pause_reason,
            "last_execution": self._last_execution,
            "interval_seconds": self.config.interval_seconds,
        }
