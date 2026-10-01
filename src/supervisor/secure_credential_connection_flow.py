from .secure_connection_interface_session import (
    SecureConnectionInterfaceSession,
)
from .secure_credential_connection_controller import (
    SecureCredentialConnectionController,
)


class SecureCredentialConnectionFlow:
    """Coordinates the complete secure credential connection flow."""

    def __init__(
        self,
        controller: SecureCredentialConnectionController | None = None,
    ) -> None:
        self.controller = (
            controller
            or SecureCredentialConnectionController()
        )

    def validate(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> bool:
        return self.controller.validate(session)

    def prepare_connection(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> dict:
        self.validate(session)

        credential_ref = self.controller.get_credential_reference(
            session.request_id
        )

        if credential_ref is None:
            raise ValueError(
                "Credential reference is not available"
            )

        return {
            "request_id": session.request_id,
            "session_id": session.session_id,
            "credential_ref": credential_ref,
            "status": "ready",
        }

    def is_ready(self, request_id: str) -> bool:
        return self.controller.is_ready(request_id)

    def remove(
        self,
        request_id: str,
        delete_credential: bool = False,
    ) -> bool:
        return self.controller.remove(
            request_id=request_id,
            delete_credential=delete_credential,
        )
