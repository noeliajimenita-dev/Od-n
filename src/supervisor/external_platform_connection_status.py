from .external_platform_connector_service import (
    ExternalPlatformConnectorService,
)
from .external_account_connection import ExternalAccountConnection


class ExternalPlatformConnectionStatus:
    """Provides status information for external platform connections."""

    def __init__(
        self,
        connector_service: ExternalPlatformConnectorService | None = None,
    ) -> None:
        self.connector_service = (
            connector_service
            or ExternalPlatformConnectorService()
        )

    def get_status(
        self,
        account: ExternalAccountConnection,
    ) -> dict:
        connector = self.connector_service.get(account.service)

        return {
            "account_id": account.account_id,
            "service": account.service,
            "username": account.username,
            "connected": account.is_connected,
            "ready": account.is_ready,
            "verified": account.verified,
            "connector_available": connector is not None,
            "supported_actions": (
                []
                if connector is None
                else getattr(connector, "supported_actions", [])
            ),
        }

    def is_supported(self, service_name: str) -> bool:
        if not service_name.strip():
            return False

        return self.connector_service.exists(service_name)

    def list_supported_platforms(self) -> list[str]:
        return self.connector_service.list_services()

    def is_ready(
        self,
        account: ExternalAccountConnection,
    ) -> bool:
        return (
            account.is_ready
            and self.connector_service.exists(account.service)
  )
