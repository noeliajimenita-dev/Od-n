from .account_connection_session import AccountConnectionSession
from .account_connection_session_repository import (
    AccountConnectionSessionRepository,
)


class AccountConnectionSessionService:
    """Manages account connection session lifecycle."""

    def __init__(
        self,
        repository: AccountConnectionSessionRepository | None = None,
    ) -> None:
        self.repository = (
            repository or AccountConnectionSessionRepository()
        )

    def create_session(
        self,
        session_id: str,
        request_id: str,
        service: str,
    ) -> AccountConnectionSession:
        if self.repository.exists(session_id):
            raise ValueError(
                f"Connection session already exists: {session_id}"
            )

        session = AccountConnectionSession(
            session_id=session_id,
            request_id=request_id,
            service=service,
        )

        self.repository.save(session)
        return session

    def wait_for_user(
        self,
        session_id: str,
    ) -> AccountConnectionSession:
        session = self._get_session(session_id)

        session.mark_waiting_for_user()
        self.repository.update(session)

        return session

    def mark_ready(
        self,
        session_id: str,
    ) -> AccountConnectionSession:
        session = self._get_session(session_id)

        session.mark_ready()
        self.repository.update(session)

        return session

    def complete(
        self,
        session_id: str,
    ) -> AccountConnectionSession:
        session = self._get_session(session_id)

        session.mark_completed()
        self.repository.update(session)

        return session

    def cancel(
        self,
        session_id: str,
    ) -> AccountConnectionSession:
        session = self._get_session(session_id)

        session.mark_cancelled()
        self.repository.update(session)

        return session

    def get(
        self,
        session_id: str,
    ) -> AccountConnectionSession | None:
        return self.repository.get(session_id)

    def get_waiting_for_user(
        self,
    ) -> list[AccountConnectionSession]:
        return self.repository.list_waiting_for_user()

    def get_active(
        self,
    ) -> list[AccountConnectionSession]:
        return self.repository.list_active()

    def _get_session(
        self,
        session_id: str,
    ) -> AccountConnectionSession:
        session = self.repository.get(session_id)

        if session is None:
            raise KeyError(
                f"Connection session not found: {session_id}"
            )

        return session
