from typing import Any

from .account_connection_manager import AccountConnectionManager


class AccountConnectionStatus:
    """Provides the current status of connected external accounts."""

    def __init__(
        self,
        connection_manager: AccountConnectionManager | None = None,
    ) -> None:
        self.connection_manager = (
            connection_manager or AccountConnectionManager()
        )

    def get_status(self, account_id: str) -> dict[str, Any]:
        account = self.connection_manager.get_account(account_id)

        if account is None:
            return {
                "account_id": account_id,
                "exists": False,
                "status": "not_found",
                "connected": False,
                "verification_required": False,
            }

        return {
            "account_id": account.account_id,
            "service": account.service,
            "username": account.username,
            "exists": True,
            "status": account.status,
            "connected": account.is_connected(),
            "verification_required": account.needs_verification(),
            "verification_type": account.verification_type,
            "credentials_available": (
                self.connection_manager.has_credentials(account.account_id)
            ),
        }

    def get_all_statuses(self) -> list[dict[str, Any]]:
        accounts = self.connection_manager.account_service.repository.list_all()

        return [
            self.get_status(account.account_id)
            for account in accounts
        ]

    def is_ready(self, account_id: str) -> bool:
        status = self.get_status(account_id)

        return (
            status["exists"]
            and status["connected"]
            and not status["verification_required"]
            and status["credentials_available"]
      )
