from typing import Any

from .secure_connection_interface_session import (
    SecureConnectionInterfaceSession,
)
from .secure_credential_connection_flow import (
    SecureCredentialConnectionFlow,
)


class SecureCredentialConnectionStatus:
    """Provides consolidated status for secure credential connections."""

    def __init__(
        self,
        flow: SecureCredentialConnectionFlow | None = None,
    ) -> None:
        self.flow = (
            flow
            or SecureCredentialConnectionFlow()
        )

    def get_status(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> dict[str, Any]:
        credentials_ready = False

        if session.is_active:
            credentials_ready = self.flow.is_ready(
                session.request_id
            )

        return {
            "session_id": session.session_id,
            "request_id": session.request_id,
            "session_status": session.status,
            "session_active": session.is_active,
            "credentials_ready": credentials_ready,
            "connection_ready": (
                session.is_active and credentials_ready
            ),
        }

    def is_ready(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> bool:
        status = self.get_status(session)
        return bool(status["connection_ready"])
