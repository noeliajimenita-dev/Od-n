from .connected_account import ConnectedAccount


class ConnectedAccountRepository:
    """Stores and manages connected external accounts."""

    def __init__(self) -> None:
        self._accounts: dict[str, ConnectedAccount] = {}

    def save(self, account: ConnectedAccount) -> None:
        if not isinstance(account, ConnectedAccount):
            raise TypeError("account must be a ConnectedAccount")

        self._accounts[account.account_id] = account

    def get(self, account_id: str) -> ConnectedAccount | None:
        return self._accounts.get(account_id)

    def exists(self, account_id: str) -> bool:
        return account_id in self._accounts

    def update(self, account: ConnectedAccount) -> None:
        if not self.exists(account.account_id):
            raise KeyError(
                f"Connected account not found: {account.account_id}"
            )

        self._accounts[account.account_id] = account

    def delete(self, account_id: str) -> None:
        self._accounts.pop(account_id, None)

    def list_all(self) -> list[ConnectedAccount]:
        return list(self._accounts.values())

    def list_connected(self) -> list[ConnectedAccount]:
        return [
            account
            for account in self._accounts.values()
            if account.is_connected()
        ]

    def count(self) -> int:
        return len(self._accounts)

    def count_connected(self) -> int:
        return len(self.list_connected())

    def clear(self) -> None:
        self._accounts.clear()
