from src.supervisor.session_state import SessionState


class SessionRepository:
    """Stores and manages Supervisor sessions."""

    def __init__(self):
        self._sessions: dict[str, SessionState] = {}

    def save(self, session: SessionState) -> SessionState:
        if not isinstance(session, SessionState):
            raise TypeError("Expected a SessionState instance")

        if not session.session_id or not session.session_id.strip():
            raise ValueError("Session ID cannot be empty")

        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> SessionState | None:
        if not session_id or not session_id.strip():
            return None

        return self._sessions.get(session_id.strip())

    def exists(self, session_id: str) -> bool:
        return self.get(session_id) is not None

    def delete(self, session_id: str) -> bool:
        if not session_id or not session_id.strip():
            return False

        return self._sessions.pop(session_id.strip(), None) is not None

    def list_sessions(self) -> list[SessionState]:
        return list(self._sessions.values())

    def count(self) -> int:
        return len(self._sessions)

    def clear(self) -> None:
        self._sessions.clear()
