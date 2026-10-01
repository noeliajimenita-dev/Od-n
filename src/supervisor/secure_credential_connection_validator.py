from .secure_connection_interface_session import (
    SecureConnectionInterfaceSession,
)
from .secure_credential_connection_service import (
    SecureCredentialConnectionService,
)


class SecureCredentialConnectionValidator:
    """Validates the prerequisites for a secure account connection."""

    def __init__(
        self,
        credential_connection_service: (
            SecureCredentialConnectionService | None
        ) = None,
    ) -> None:
        self.credential_connection_service = (
            credential_connection_service
            or SecureCredentialConnectionService()
        )

    def validate_session(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> bool:
        if not isinstance(
            session,
            SecureConnectionInterfaceSession,
        ):
            raise TypeError(
                "session must be a SecureConnectionInterfaceSession"
            )

        if not session.is_active:
            raise ValueError(
                "Connection session is not active"
            )

        if not session.request_id.strip():
            raise ValueError(
                "session request_id cannot be empty"
            )

        return True

    def validate_credentials(
        self,
        request_id: str,
    ) -> bool:
        if not request_id.strip():
            raise ValueError(
                "request_id cannot be empty"
            )

        if not self.credential_connection_service.is_ready(
            request_id
        ):
            raise ValueError(
                "Credentials are not available for connection"
            )

        return True

    def validate_connection(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> bool:
        self.validate_session(session)
        self.validate_credentials(session.request_id)
        return True
