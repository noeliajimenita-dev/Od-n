from .external_account_connection import ExternalAccountConnection
from .external_account_connection_repository import (
    ExternalAccountConnectionRepository,
)


class ExternalAccountConnectionService:
    """Service layer for operational external accounts."""

    def __init__(
        self,
        repository: ExternalAccountConnectionRepository | None = None,
    ) -> None:
        self.repository = (
            repository or ExternalAccountConnectionRepository()
        )

    def register(
        self,
        account: ExternalAccountConnection,
    ) -> ExternalAccountConnection:
        return self.repository.save(account)

    def get(
        self,
        account_id: str,
    ) -> ExternalAccountConnection | None:
        return self.repository.get(account_id)

    def verify(
        self,
        account_id: str,
    ) -> ExternalAccountConnection:
        account = self._require_account(account_id)
        account.verify()
        return self.repository.update(account)

    def disconnect(
        self,
        account_id: str,
    ) -> ExternalAccountConnection:
        account = self._require_account(account_id)
        account.disconnect()
        return self.repository.update(account)

    def reconnect(
        self,
        account_id: str,
    ) -> ExternalAccountConnection:
        account = self._require_account(account_id)
        account.reconnect()
        return self.repository.update(account)

    def is_ready(self, account_id: str) -> bool:
        account = self.repository.get(account_id)

        if account is None:
            return False

        return account.is_ready

    def get_ready_accounts(
        self,
    ) -> list[ExternalAccountConnection]:
        return self.repository.list_ready()

    def count_ready(self) -> int:
        return self.repository.count_ready()

    def _require_account(
        self,
        account_id: str,
    ) -> ExternalAccountConnection:
        account = self.repository.get(account_id)

        if account is None:
            raise ValueError(
                f"Account not found: {account_id}"
            )

        return account
