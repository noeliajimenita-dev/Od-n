from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from .odin_daily_log import OdinDailyLog


class OdinLogService:
    """
    Servicio central para los registros diarios de ODIN.

    Mantiene los logs por fecha y bot y ofrece operaciones
    para registrar actividad y generar resúmenes.
    """

    def __init__(self) -> None:
        self._logs: dict[tuple[date, str], OdinDailyLog] = {}

    def get_or_create(
        self,
        bot_id: str,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        if not bot_id or not bot_id.strip():
            raise ValueError("bot_id cannot be empty")

        current_date = log_date or date.today()
        key = (current_date, bot_id)

        if key not in self._logs:
            self._logs[key] = OdinDailyLog(
                log_date=current_date,
                bot_id=bot_id,
            )

        return self._logs[key]

    def record_work(
        self,
        bot_id: str,
        hours: float,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        log = self.get_or_create(
            bot_id,
            log_date,
        )
        log.add_work_hours(hours)
        return log

    def record_proposal(
        self,
        bot_id: str,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        log = self.get_or_create(
            bot_id,
            log_date,
        )
        log.record_proposal()
        return log

    def record_job(
        self,
        bot_id: str,
        income: float = 0.0,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        log = self.get_or_create(
            bot_id,
            log_date,
        )
        log.record_completed_job(income)
        return log

    def record_tokens(
        self,
        bot_id: str,
        tokens: int,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        log = self.get_or_create(
            bot_id,
            log_date,
        )
        log.record_tokens(tokens)
        return log

    def record_error(
        self,
        bot_id: str,
        error: str,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        log = self.get_or_create(
            bot_id,
            log_date,
        )
        log.record_error(error)
        return log

    def record_event(
        self,
        bot_id: str,
        event_type: str,
        details: dict[str, Any] | None = None,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        log = self.get_or_create(
            bot_id,
            log_date,
        )
        log.record_event(
            event_type,
            details,
        )
        return log

    def set_status(
        self,
        bot_id: str,
        status: str,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        log = self.get_or_create(
            bot_id,
            log_date,
        )
        log.set_status(status)
        return log

    def set_quota_reset(
        self,
        bot_id: str,
        reset_at: datetime,
        log_date: date | None = None,
    ) -> OdinDailyLog:
        log = self.get_or_create(
            bot_id,
            log_date,
        )
        log.set_quota_reset(reset_at)
        return log

    def get(
        self,
        bot_id: str,
        log_date: date | None = None,
    ) -> OdinDailyLog | None:
        current_date = log_date or date.today()
        return self._logs.get(
            (current_date, bot_id)
        )

    def get_today(
        self,
        bot_id: str,
    ) -> OdinDailyLog:
        return self.get_or_create(bot_id)

    def list_for_date(
        self,
        log_date: date,
    ) -> list[OdinDailyLog]:
        return [
            log
            for (stored_date, _),
            log in self._logs.items()
            if stored_date == log_date
        ]

    def list_for_bot(
        self,
        bot_id: str,
    ) -> list[OdinDailyLog]:
        return [
            log
            for (_, stored_bot),
            log in self._logs.items()
            if stored_bot == bot_id
        ]

    def list_recent(
        self,
        days: int = 7,
    ) -> list[OdinDailyLog]:
        if days <= 0:
            raise ValueError(
                "days must be greater than zero"
            )

        today = date.today()
        start = today - timedelta(days=days - 1)

        return [
            log
            for (stored_date, _),
            log in self._logs.items()
            if start <= stored_date <= today
        ]

    def summary(
        self,
        log_date: date | None = None,
    ) -> dict[str, Any]:
        current_date = log_date or date.today()
        logs = self.list_for_date(current_date)

        return {
            "date": current_date.isoformat(),
            "bots": len(logs),
            "hours_worked": sum(
                log.hours_worked
                for log in logs
            ),
            "proposals_sent": sum(
                log.proposals_sent
                for log in logs
            ),
            "jobs_completed": sum(
                log.jobs_completed
                for log in logs
            ),
            "income": sum(
                log.income
                for log in logs
            ),
            "tokens_used": sum(
                log.tokens_used
                for log in logs
            ),
            "errors": sum(
                len(log.errors)
                for log in logs
            ),
        }

    def export_date(
        self,
        log_date: date | None = None,
    ) -> list[dict[str, Any]]:
        current_date = log_date or date.today()

        return [
            log.to_dict()
            for log in self.list_for_date(
                current_date
            )
        ]

    def count(self) -> int:
        return len(self._logs)

    def clear(self) -> None:
        self._logs.clear()
