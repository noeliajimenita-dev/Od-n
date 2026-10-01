from .external_account_connection_service import (
    ExternalAccountConnectionService,
)


class ExternalAccountConnectionStatus:
    """Provides operational status for external accounts."""

    def __init__(
        self,
        service: ExternalAccountConnectionService | None = None,
    ) -> None:
        self.service = service or ExternalAccountConnectionService()

    def get_status(self, account_id: str) -> dict:
        account = self.service.get(account_id)

        if account is None:
            return {
                "account_id": account_id,
                "exists": False,
                "connected": False,
                "verified": False,
                "ready": False,
            }

        return {
            "account_id": account.account_id,
            "service": account.service,
            "username": account.username,
            "exists": True,
            "connected": account.is_connected,
            "verified": account.verified,
            "ready": account.is_ready,
            "status": account.status,
        }

    def get_all_statuses(self) -> list[dict]:
        return [
            self.get_status(account.account_id)
            for account in self.service.repository.list_all()
        ]

    def get_ready_count(self) -> int:
        return self.service.count_ready()

    def has_ready_accounts(self) -> bool:
        return self.get_ready_count() > 0
