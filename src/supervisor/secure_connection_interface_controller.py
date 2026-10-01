from .secure_connection_interface import SecureConnectionInterfaceRequest
from .secure_connection_interface_service import (
    SecureConnectionInterfaceService,
)
from .secure_connection_interface_session_service import (
    SecureConnectionInterfaceSessionService,
)
from .secure_connection_interface_security import (
    SecureConnectionInterfaceSecurity,
)


class SecureConnectionInterfaceController:
    """Coordinates secure connection interface operations."""

    def __init__(
        self,
        interface_service: SecureConnectionInterfaceService | None = None,
        session_service: SecureConnectionInterfaceSessionService | None = None,
        security: SecureConnectionInterfaceSecurity | None = None,
    ) -> None:
        self.interface_service = (
            interface_service or SecureConnectionInterfaceService()
        )
        self.session_service = (
            session_service
            or SecureConnectionInterfaceSessionService()
        )
        self.security = (
            security or SecureConnectionInterfaceSecurity()
        )

    def start(
        self,
        request_id: str,
        service: str,
        username: str,
        interface_token: str,
        session_id: str,
    ) -> dict:
        request = self.interface_service.create_connection_request(
            request_id=request_id,
            service=service,
            username=username,
            interface_token=interface_token,
        )

        session = self.session_service.create_session(
            session_id=session_id,
            request_id=request_id,
            interface_token=interface_token,
        )

        return {
            "request": request.to_dict(),
            "session": session.to_dict(),
            "status": "ready",
        }

    def authorize_access(
        self,
        session_id: str,
        provided_token: str,
    ) -> bool:
        session = self.session_service.get_session(session_id)

        if session is None:
            raise ValueError(
                f"Session not found: {session_id}"
            )

        return self.security.authorize_interface_access(
            session=session,
            provided_token=provided_token,
        )

    def complete(
        self,
        request_id: str,
        session_id: str,
    ) -> dict:
        request = self.interface_service.complete_request(request_id)
        session = self.session_service.complete_session(session_id)

        return {
            "request": request.to_dict(),
            "session": session.to_dict(),
            "status": "completed",
        }

    def cancel(
        self,
        request_id: str,
        session_id: str,
    ) -> dict:
        request = self.interface_service.cancel_request(request_id)
        session = self.session_service.cancel_session(session_id)

        return {
            "request": request.to_dict(),
            "session": session.to_dict(),
            "status": "cancelled",
        }
