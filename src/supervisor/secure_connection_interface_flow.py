from .secure_connection_interface_controller import (
    SecureConnectionInterfaceController,
)
from .secure_connection_interface_validator import (
    SecureConnectionInterfaceValidator,
)


class SecureConnectionInterfaceFlow:
    """Coordinates the complete secure connection interface flow."""

    def __init__(
        self,
        controller: SecureConnectionInterfaceController | None = None,
        validator: SecureConnectionInterfaceValidator | None = None,
    ) -> None:
        self.controller = (
            controller or SecureConnectionInterfaceController()
        )
        self.validator = (
            validator or SecureConnectionInterfaceValidator()
        )

    def start(
        self,
        request_id: str,
        service: str,
        username: str,
        interface_token: str,
        session_id: str,
    ) -> dict:
        result = self.controller.start(
            request_id=request_id,
            service=service,
            username=username,
            interface_token=interface_token,
            session_id=session_id,
        )

        return result

    def authorize(
        self,
        session_id: str,
        provided_token: str,
    ) -> bool:
        return self.controller.authorize_access(
            session_id=session_id,
            provided_token=provided_token,
        )

    def complete(
        self,
        request_id: str,
        session_id: str,
    ) -> dict:
        return self.controller.complete(
            request_id=request_id,
            session_id=session_id,
        )

    def cancel(
        self,
        request_id: str,
        session_id: str,
    ) -> dict:
        return self.controller.cancel(
            request_id=request_id,
            session_id=session_id,
      )
