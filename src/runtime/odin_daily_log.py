from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass
class OdinDailyLog:
    log_date: date
    bot_id: str

    hours_worked: float = 0.0
    proposals_sent: int = 0
    jobs_completed: int = 0
    income: float = 0.0
    tokens_used: int = 0

    errors: list[str] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    status: str = "idle"
    quota_reset_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.bot_id or not self.bot_id.strip():
            raise ValueError("bot_id cannot be empty")

        if self.hours_worked < 0:
            raise ValueError("hours_worked cannot be negative")

        if self.proposals_sent < 0:
            raise ValueError("proposals_sent cannot be negative")

        if self.jobs_completed < 0:
            raise ValueError("jobs_completed cannot be negative")

        if self.income < 0:
            raise ValueError("income cannot be negative")

        if self.tokens_used < 0:
            raise ValueError("tokens_used cannot be negative")

    def add_work_hours(self, hours: float) -> None:
        if hours < 0:
            raise ValueError("hours cannot be negative")

        self.hours_worked += hours

    def record_proposal(self) -> None:
        self.proposals_sent += 1

    def record_completed_job(
        self,
        income: float = 0.0,
    ) -> None:
        if income < 0:
            raise ValueError(
                "income cannot be negative"
            )

        self.jobs_completed += 1
        self.income += income

    def record_tokens(
        self,
        tokens: int,
    ) -> None:
        if tokens < 0:
            raise ValueError(
                "tokens cannot be negative"
            )

        self.tokens_used += tokens

    def record_error(
        self,
        error: str,
    ) -> None:
        if not error or not error.strip():
            return

        self.errors.append(
            error.strip()
        )

        self.status = "error"

    def record_event(
        self,
        event_type: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        if not event_type or not event_type.strip():
            raise ValueError(
                "event_type cannot be empty"
            )

        self.events.append(
            {
                "timestamp": datetime.now().isoformat(),
                "type": event_type.strip(),
                "details": details or {},
            }
        )

    def set_status(
        self,
        status: str,
    ) -> None:
        if not status or not status.strip():
            raise ValueError(
                "status cannot be empty"
            )

        self.status = status.strip()

    def set_quota_reset(
        self,
        reset_at: datetime,
    ) -> None:
        self.quota_reset_at = reset_at

    def summary(self) -> dict[str, Any]:
        return {
            "date": self.log_date.isoformat(),
            "bot_id": self.bot_id,
            "hours_worked": self.hours_worked,
            "proposals_sent": self.proposals_sent,
            "jobs_completed": self.jobs_completed,
            "income": self.income,
            "tokens_used": self.tokens_used,
            "errors": len(self.errors),
            "status": self.status,
            "quota_reset_at": (
                self.quota_reset_at.isoformat()
                if self.quota_reset_at
                else None
            ),
            "events": len(self.events),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.log_date.isoformat(),
            "bot_id": self.bot_id,
            "hours_worked": self.hours_worked,
            "proposals_sent": self.proposals_sent,
            "jobs_completed": self.jobs_completed,
            "income": self.income,
            "tokens_used": self.tokens_used,
            "errors": list(self.errors),
            "events": list(self.events),
            "status": self.status,
            "quota_reset_at": (
                self.quota_reset_at.isoformat()
                if self.quota_reset_at
                else None
            ),
          }
