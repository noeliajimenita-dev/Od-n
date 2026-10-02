from __future__ import annotations

from .platform_account import PlatformAccount
from .platform_account_repository import PlatformAccountRepository


class PlatformAccountService:
    """Servicio central para gestionar cuentas de plataformas."""

    def __init__(
        self,
        repository: PlatformAccountRepository,
    ) -> None:
        if repository is None:
            raise ValueError("repository cannot be None")

        self.repository = repository

    def register(
        self,
        account: PlatformAccount,
    ) -> PlatformAccount:
        if account is None:
            raise ValueError("account cannot be None")

        if self.repository.exists(account.account_id):
            raise ValueError(
                f"Account already exists: {account.account_id}"
            )

        return self.repository.save(account)

    def get(
        self,
        account_id: str,
    ) -> PlatformAccount | None:
        return self.repository.get(account_id)

    def connect(
        self,
        account_id: str,
    ) -> PlatformAccount:
        account = self._require(account_id)

        account.connect()
        return self.repository.save(account)

    def disconnect(
        self,
        account_id: str,
    ) -> PlatformAccount:
        account = self._require(account_id)

        account.disconnect()
        return self.repository.save(account)

    def verify(
        self,
        account_id: str,
    ) -> PlatformAccount:
        account = self._require(account_id)

        account.verify()
        return self.repository.save(account)

    def unverify(
        self,
        account_id: str,
    ) -> PlatformAccount:
        account = self._require(account_id)

        account.unverify()
        return self.repository.save(account)

    def add_capability(
        self,
        account_id: str,
        capability: str,
    ) -> PlatformAccount:
        account = self._require(account_id)

        account.add_capability(capability)
        return self.repository.save(account)

    def remove_capability(
        self,
        account_id: str,
        capability: str,
    ) -> bool:
        account = self._require(account_id)

        changed = account.remove_capability(capability)

        if changed:
            self.repository.save(account)

        return changed

    def supports(
        self,
        account_id: str,
        capability: str,
    ) -> bool:
        account = self.get(account_id)

        if account is None:
            return False

        return account.supports(capability)

    def is_ready(
        self,
        account_id: str,
    ) -> bool:
        account = self.get(account_id)

        if account is None:
            return False

        return account.is_ready()

    def get_ready_accounts(
        self,
        platform: str | None = None,
        capability: str | None = None,
    ) -> list[PlatformAccount]:
        accounts = self.repository.list_ready()

        if platform:
            platform = platform.strip().lower()
            accounts = [
                account
                for account in accounts
                if account.platform.lower() == platform
            ]

        if capability:
            capability = capability.strip()
            accounts = [
                account
                for account in accounts
                if account.supports(capability)
            ]

        return accounts

    def list_by_platform(
        self,
        platform: str,
    ) -> list[PlatformAccount]:
        return self.repository.list_by_platform(platform)

    def list_all(self) -> list[PlatformAccount]:
        return self.repository.list_all()

    def count(self) -> int:
        return self.repository.count()

    def count_ready(self) -> int:
        return self.repository.count_ready()

    def remove(self, account_id: str) -> bool:
        return self.repository.delete(account_id)

    def _require(
        self,
        account_id: str,
    ) -> PlatformAccount:
        account = self.get(account_id)

        if account is None:
            raise ValueError(
                f"Account not found: {account_id}"
            )

        return account

    def __repr__(self) -> str:
        return (
            "PlatformAccountService("
            f"accounts={self.count()}, "
            f"ready={self.count_ready()}"
            ")"
  )
