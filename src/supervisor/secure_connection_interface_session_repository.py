from .secure_connection_interface_session import (
    SecureConnectionInterfaceSession,
)


class SecureConnectionInterfaceSessionRepository:
    """In-memory repository for secure connection interface sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, SecureConnectionInterfaceSession] = {}

    def save(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> SecureConnectionInterfaceSession:
        self._sessions[session.session_id] = session
        return session

    def get(
        self,
        session_id: str,
    ) -> SecureConnectionInterfaceSession | None:
        return self._sessions.get(session_id)

    def exists(self, session_id: str) -> bool:
        return session_id in self._sessions

    def update(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> SecureConnectionInterfaceSession:
        if session.session_id not in self._sessions:
            raise ValueError(
                f"Session not found: {session.session_id}"
            )

        self._sessions[session.session_id] = session
        return session

    def delete(self, session_id: str) -> bool:
        if session_id not in self._sessions:
            return False

        del self._sessions[session_id]
        return True

    def list_all(self) -> list[SecureConnectionInterfaceSession]:
        return list(self._sessions.values())

    def list_active(self) -> list[SecureConnectionInterfaceSession]:
        return [
            session
            for session in self._sessions.values()
            if session.is_active
        ]

    def list_completed(self) -> list[SecureConnectionInterfaceSession]:
        return [
            session
            for session in self._sessions.values()
            if session.is_completed
        ]

    def list_expired(self) -> list[SecureConnectionInterfaceSession]:
        return [
            session
            for session in self._sessions.values()
            if session.is_expired
        ]

    def count(self) -> int:
        return len(self._sessions)

    def count_active(self) -> int:
        return len(self.list_active())

    def clear(self) -> None:
        self._sessions.clear()
