from .connected_account import ConnectedAccount
from .connected_account_repository import ConnectedAccountRepository


class ConnectedAccountService:
    """Manages the lifecycle of connected external accounts."""

    def __init__(
        self,
        repository: ConnectedAccountRepository | None = None,
    ) -> None:
        self.repository = repository or ConnectedAccountRepository()

    def connect(
        self,
        account_id: str,
        service: str,
        username: str,
        credential_ref: str,
    ) -> ConnectedAccount:
        if self.repository.exists(account_id):
            raise ValueError(
                f"Connected account already exists: {account_id}"
            )

        account = ConnectedAccount(
            account_id=account_id,
            service=service,
            username=username,
            credential_ref=credential_ref,
        )

        self.repository.save(account)
        return account

    def disconnect(self, account_id: str) -> ConnectedAccount:
        account = self._get_account(account_id)
        account.mark_disconnected()
        self.repository.update(account)
        return account

    def reconnect(self, account_id: str) -> ConnectedAccount:
        account = self._get_account(account_id)
        account.mark_connected()
        self.repository.update(account)
        return account

    def request_verification(
        self,
        account_id: str,
        verification_type: str,
    ) -> ConnectedAccount:
        account = self._get_account(account_id)
        account.request_verification(verification_type)
        self.repository.update(account)
        return account

    def get(self, account_id: str) -> ConnectedAccount | None:
        return self.repository.get(account_id)

    def get_connected(self) -> list[ConnectedAccount]:
        return self.repository.list_connected()

    def is_connected(self, account_id: str) -> bool:
        account = self.repository.get(account_id)
        return account is not None and account.is_connected()

    def _get_account(self, account_id: str) -> ConnectedAccount:
        account = self.repository.get(account_id)

        if account is None:
            raise KeyError(
                f"Connected account not found: {account_id}"
            )

        return account
