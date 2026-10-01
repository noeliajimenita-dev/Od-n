from .secure_connection_interface_session import (
    SecureConnectionInterfaceSession,
)


class SecureConnectionInterfaceSecurity:
    """Security checks for secure connection interface sessions."""

    ALLOWED_ACTIVE_STATUS = "active"

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

        if not session.session_id.strip():
            raise ValueError("session_id cannot be empty")

        if not session.request_id.strip():
            raise ValueError("request_id cannot be empty")

        if not session.interface_token.strip():
            raise ValueError("interface_token cannot be empty")

        if session.status != self.ALLOWED_ACTIVE_STATUS:
            raise ValueError(
                "Only active sessions can access the secure interface"
            )

        return True

    def authorize_interface_access(
        self,
        session: SecureConnectionInterfaceSession,
        provided_token: str,
    ) -> bool:
        self.validate_session(session)

        if not provided_token:
            raise ValueError("interface token is required")

        if provided_token != session.interface_token:
            raise PermissionError(
                "Invalid interface token"
            )

        return True

    def can_enter_credentials(
        self,
        session: SecureConnectionInterfaceSession,
        provided_token: str,
    ) -> bool:
        return self.authorize_interface_access(
            session=session,
            provided_token=provided_token,
        )
