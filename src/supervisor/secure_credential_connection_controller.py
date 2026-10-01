from .secure_connection_interface_session import (
    SecureConnectionInterfaceSession,
)
from .secure_credential_connection_service import (
    SecureCredentialConnectionService,
)
from .secure_credential_connection_validator import (
    SecureCredentialConnectionValidator,
)


class SecureCredentialConnectionController:
    """Coordinates secure credential connection operations."""

    def __init__(
        self,
        connection_service: SecureCredentialConnectionService | None = None,
        validator: SecureCredentialConnectionValidator | None = None,
    ) -> None:
        self.connection_service = (
            connection_service
            or SecureCredentialConnectionService()
        )
        self.validator = (
            validator
            or SecureCredentialConnectionValidator(
                credential_connection_service=self.connection_service
            )
        )

    def validate(
        self,
        session: SecureConnectionInterfaceSession,
    ) -> bool:
        return self.validator.validate_connection(session)

    def is_ready(
        self,
        request_id: str,
    ) -> bool:
        return self.connection_service.is_ready(request_id)

    def get_credential_reference(
        self,
        request_id: str,
    ) -> str | None:
        return self.connection_service.get_credential_reference(
            request_id
        )

    def remove(
        self,
        request_id: str,
        delete_credential: bool = False,
    ) -> bool:
        return self.connection_service.remove_submission(
            request_id=request_id,
            delete_credential=delete_credential,
        )
