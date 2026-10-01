from typing import Any

from src.supervisor.session_history_exporter import SessionHistoryExporter
from src.supervisor.session_history_service import SessionHistoryService


class SessionHistoryReport:
    """Builds structured reports from Supervisor session history."""

    def __init__(
        self,
        history_service: SessionHistoryService,
        exporter: SessionHistoryExporter | None = None,
    ):
        if history_service is None:
            raise ValueError("Session history service is required")

        self.history_service = history_service
        self.exporter = exporter or SessionHistoryExporter(history_service)

    def generate(self, session_id: str) -> dict[str, Any]:
        summary = self.history_service.get_event_summary(session_id)
        events = self.exporter.export_events(session_id)

        return {
            "session_id": session_id,
            "summary": summary,
            "events": events,
            "total_events": len(events),
        }

    def generate_latest(
        self,
        session_id: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        summary = self.history_service.get_event_summary(session_id)
        events = self.exporter.export_latest(
            session_id,
            limit=limit,
        )

        return {
            "session_id": session_id,
            "summary": summary,
            "latest_events": events,
            "total_events": len(events),
        }

    def is_empty(self, session_id: str) -> bool:
        return not self.history_service.has_history(session_id)
