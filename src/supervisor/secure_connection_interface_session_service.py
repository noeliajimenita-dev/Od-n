from .secure_connection_interface_session import (
    SecureConnectionInterfaceSession,
)
from .secure_connection_interface_session_repository import (
    SecureConnectionInterfaceSessionRepository,
)


class SecureConnectionInterfaceSessionService:
    """Service layer for secure connection interface sessions."""

    def __init__(
        self,
        repository: SecureConnectionInterfaceSessionRepository | None = None,
    ) -> None:
        self.repository = (
            repository
            or SecureConnectionInterfaceSessionRepository()
        )

    def create_session(
        self,
        session_id: str,
        request_id: str,
        interface_token: str,
    ) -> SecureConnectionInterfaceSession:
        session = SecureConnectionInterfaceSession(
            session_id=session_id,
            request_id=request_id,
            interface_token=interface_token,
        )

        return self.repository.save(session)

    def get_session(
        self,
        session_id: str,
    ) -> SecureConnectionInterfaceSession | None:
        return self.repository.get(session_id)

    def complete_session(
        self,
        session_id: str,
    ) -> SecureConnectionInterfaceSession:
        session = self._require_session(session_id)
        session.complete()
        return self.repository.update(session)

    def cancel_session(
        self,
        session_id: str,
    ) -> SecureConnectionInterfaceSession:
        session = self._require_session(session_id)
        session.cancel()
        return self.repository.update(session)

    def expire_session(
        self,
        session_id: str,
    ) -> SecureConnectionInterfaceSession:
        session = self._require_session(session_id)
        session.expire()
        return self.repository.update(session)

    def get_active_sessions(
        self,
    ) -> list[SecureConnectionInterfaceSession]:
        return self.repository.list_active()

    def count_active_sessions(self) -> int:
        return self.repository.count_active()

    def _require_session(
        self,
        session_id: str,
    ) -> SecureConnectionInterfaceSession:
        session = self.repository.get(session_id)

        if session is None:
            raise ValueError(
                f"Session not found: {session_id}"
            )

        return session
