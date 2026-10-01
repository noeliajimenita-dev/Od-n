from .account_connection_session import AccountConnectionSession


class AccountConnectionSessionRepository:
    """Stores and manages account connection sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, AccountConnectionSession] = {}

    def save(self, session: AccountConnectionSession) -> None:
        if not isinstance(session, AccountConnectionSession):
            raise TypeError(
                "session must be an AccountConnectionSession"
            )

        self._sessions[session.session_id] = session

    def get(self, session_id: str) -> AccountConnectionSession | None:
        return self._sessions.get(session_id)

    def exists(self, session_id: str) -> bool:
        return session_id in self._sessions

    def update(self, session: AccountConnectionSession) -> None:
        if not self.exists(session.session_id):
            raise KeyError(
                f"Connection session not found: {session.session_id}"
            )

        self._sessions[session.session_id] = session

    def delete(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def list_all(self) -> list[AccountConnectionSession]:
        return list(self._sessions.values())

    def list_waiting_for_user(self) -> list[AccountConnectionSession]:
        return [
            session
            for session in self._sessions.values()
            if session.is_waiting_for_user
        ]

    def list_active(self) -> list[AccountConnectionSession]:
        return [
            session
            for session in self._sessions.values()
            if not session.is_completed and not session.is_cancelled
        ]

    def count(self) -> int:
        return len(self._sessions)

    def clear(self) -> None:
        self._sessions.clear()
