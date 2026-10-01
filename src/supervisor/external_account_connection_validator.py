from .external_account_connection import ExternalAccountConnection
from .external_account_connection_repository import (
    ExternalAccountConnectionRepository,
)


class ExternalAccountConnectionValidator:
    """Validates operational external account connections."""

    def __init__(
        self,
        repository: ExternalAccountConnectionRepository | None = None,
    ) -> None:
        self.repository = (
            repository or ExternalAccountConnectionRepository()
        )

    def validate_account(
        self,
        account_id: str,
    ) -> ExternalAccountConnection:
        account = self.repository.get(account_id)

        if account is None:
            raise ValueError(
                f"Account not found: {account_id}"
            )

        self.validate_connection(account)
        return account

    def validate_connection(
        self,
        account: ExternalAccountConnection,
    ) -> bool:
        if not account.service.strip():
            raise ValueError("Account service cannot be empty")

        if not account.username.strip():
            raise ValueError("Account username cannot be empty")

        if not account.credential_ref.strip():
            raise ValueError(
                "Account credential reference cannot be empty"
            )

        if not account.is_connected:
            raise ValueError(
                f"Account is not connected: {account.account_id}"
            )

        return True

    def is_valid(self, account_id: str) -> bool:
        try:
            self.validate_account(account_id)
            return True
        except ValueError:
            return False

    def is_ready(self, account_id: str) -> bool:
        account = self.repository.get(account_id)

        if account is None:
            return False

        return account.is_ready
