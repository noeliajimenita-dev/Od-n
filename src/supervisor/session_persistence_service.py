from src.supervisor.session_repository import SessionRepository
from src.supervisor.session_state import SessionState


class SessionPersistenceService:
    """Provides a controlled persistence interface for Supervisor sessions."""

    def __init__(self, repository: SessionRepository):
        if repository is None:
            raise ValueError("Session repository is required")

        self.repository = repository

    def save(self, session: SessionState) -> SessionState:
        self._validate_session(session)
        return self.repository.save(session)

    def get(self, session_id: str) -> SessionState | None:
        return self.repository.get(session_id)

    def exists(self, session_id: str) -> bool:
        return self.repository.exists(session_id)

    def update(self, session: SessionState) -> SessionState:
        self._validate_session(session)

        if not self.repository.exists(session.session_id):
            raise ValueError(
                f"Session not found: {session.session_id}"
            )

        return self.repository.save(session)

    def delete(self, session_id: str) -> bool:
        return self.repository.delete(session_id)

    def list_sessions(self) -> list[SessionState]:
        return self.repository.list_sessions()

    def count(self) -> int:
        return self.repository.count()

    def clear(self) -> None:
        self.repository.clear()

    def _validate_session(self, session: SessionState) -> None:
        if not isinstance(session, SessionState):
            raise TypeError("Expected a SessionState instance")
