from .external_account_connection import ExternalAccountConnection


class ExternalAccountConnectionRepository:
    """Repository for operational external account connections."""

    def __init__(self) -> None:
        self._accounts: dict[str, ExternalAccountConnection] = {}

    def save(
        self,
        account: ExternalAccountConnection,
    ) -> ExternalAccountConnection:
        self._accounts[account.account_id] = account
        return account

    def get(
        self,
        account_id: str,
    ) -> ExternalAccountConnection | None:
        return self._accounts.get(account_id)

    def exists(self, account_id: str) -> bool:
        return account_id in self._accounts

    def update(
        self,
        account: ExternalAccountConnection,
    ) -> ExternalAccountConnection:
        if account.account_id not in self._accounts:
            raise ValueError(
                f"Account not found: {account.account_id}"
            )

        self._accounts[account.account_id] = account
        return account

    def delete(self, account_id: str) -> bool:
        if account_id not in self._accounts:
            return False

        del self._accounts[account_id]
        return True

    def list_all(self) -> list[ExternalAccountConnection]:
        return list(self._accounts.values())

    def list_connected(self) -> list[ExternalAccountConnection]:
        return [
            account
            for account in self._accounts.values()
            if account.is_connected
        ]

    def list_ready(self) -> list[ExternalAccountConnection]:
        return [
            account
            for account in self._accounts.values()
            if account.is_ready
        ]

    def count(self) -> int:
        return len(self._accounts)

    def count_ready(self) -> int:
        return len(self.list_ready())

    def clear(self) -> None:
        self._accounts.clear()
