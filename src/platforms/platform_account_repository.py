from __future__ import annotations

from .platform_account import PlatformAccount


class PlatformAccountRepository:
    """Repositorio en memoria de cuentas de plataformas."""

    def __init__(self) -> None:
        self._accounts: dict[str, PlatformAccount] = {}

    def save(self, account: PlatformAccount) -> PlatformAccount:
        if account is None:
            raise ValueError("account cannot be None")

        self._accounts[account.account_id] = account
        return account

    def get(self, account_id: str) -> PlatformAccount | None:
        if not account_id or not account_id.strip():
            return None

        return self._accounts.get(account_id)

    def exists(self, account_id: str) -> bool:
        return self.get(account_id) is not None

    def delete(self, account_id: str) -> bool:
        if account_id not in self._accounts:
            return False

        del self._accounts[account_id]
        return True

    def list_all(self) -> list[PlatformAccount]:
        return list(self._accounts.values())

    def list_by_platform(
        self,
        platform: str,
    ) -> list[PlatformAccount]:
        platform = platform.strip().lower()

        return [
            account
            for account in self._accounts.values()
            if account.platform.lower() == platform
        ]

    def list_connected(self) -> list[PlatformAccount]:
        return [
            account
            for account in self._accounts.values()
            if account.is_connected()
        ]

    def list_ready(self) -> list[PlatformAccount]:
        return [
            account
            for account in self._accounts.values()
            if account.is_ready()
        ]

    def list_with_capability(
        self,
        capability: str,
    ) -> list[PlatformAccount]:
        capability = capability.strip()

        return [
            account
            for account in self._accounts.values()
            if account.supports(capability)
        ]

    def count(self) -> int:
        return len(self._accounts)

    def count_connected(self) -> int:
        return len(self.list_connected())

    def count_ready(self) -> int:
        return len(self.list_ready())

    def clear(self) -> None:
        self._accounts.clear()

    def __repr__(self) -> str:
        return (
            "PlatformAccountRepository("
            f"accounts={self.count()}"
            ")"
      )
