from .external_account_connection import ExternalAccountConnection
from .external_account_connection_service import ExternalAccountConnectionService
from .external_account_connection_validator import (
    ExternalAccountConnectionValidator,
)


class ExternalAccountConnectionController:
    """Coordinates external account connection operations."""

    def __init__(
        self,
        service: ExternalAccountConnectionService | None = None,
        validator: ExternalAccountConnectionValidator | None = None,
    ) -> None:
        self.service = service or ExternalAccountConnectionService()
        self.validator = validator or ExternalAccountConnectionValidator(
            self.service.repository
        )

    def register(
        self,
        account: ExternalAccountConnection,
    ) -> ExternalAccountConnection:
        self.validator.validate_connection(account)
        return self.service.register(account)

    def verify(self, account_id: str) -> ExternalAccountConnection:
        self.validator.validate_account(account_id)
        return self.service.verify(account_id)

    def disconnect(self, account_id: str) -> ExternalAccountConnection:
        self.validator.validate_account(account_id)
        return self.service.disconnect(account_id)

    def reconnect(self, account_id: str) -> ExternalAccountConnection:
        account = self.service.reconnect(account_id)
        self.validator.validate_connection(account)
        return account

    def get(
        self,
        account_id: str,
    ) -> ExternalAccountConnection | None:
        return self.service.get(account_id)

    def is_ready(self, account_id: str) -> bool:
        return self.service.is_ready(account_id)

    def get_ready_accounts(self) -> list[ExternalAccountConnection]:
        return self.service.get_ready_accounts()
