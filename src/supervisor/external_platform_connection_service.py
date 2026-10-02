from .external_account_connection import ExternalAccountConnection
from .external_platform_connector_service import (
    ExternalPlatformConnectorService,
)


class ExternalPlatformConnectionService:
    """Coordinates connections through platform connectors."""

    def __init__(
        self,
        connector_service: ExternalPlatformConnectorService | None = None,
    ) -> None:
        self.connector_service = (
            connector_service
            or ExternalPlatformConnectorService()
        )

    def connect(
        self,
        account: ExternalAccountConnection,
    ) -> bool:
        connector = self.connector_service.get_for_service(
            account.service
        )

        return connector.connect(account)

    def disconnect(
        self,
        account: ExternalAccountConnection,
    ) -> None:
        connector = self.connector_service.get_for_service(
            account.service
        )

        connector.disconnect(account)

    def is_supported(self, service_name: str) -> bool:
        return self.connector_service.exists(service_name)

    def get_connector(self, service_name: str):
        return self.connector_service.get_for_service(
            service_name
        )
