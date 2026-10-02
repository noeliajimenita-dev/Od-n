from .external_platform_connector import ExternalPlatformConnector
from .external_platform_connector_service import (
    ExternalPlatformConnectorService,
)


class ExternalPlatformManager:
    """Central manager for external platform connectors."""

    def __init__(
        self,
        connector_service: ExternalPlatformConnectorService | None = None,
    ) -> None:
        self.connector_service = (
            connector_service
            or ExternalPlatformConnectorService()
        )

    def register(
        self,
        connector: ExternalPlatformConnector,
    ) -> ExternalPlatformConnector:
        return self.connector_service.register(connector)

    def get(
        self,
        service_name: str,
    ) -> ExternalPlatformConnector | None:
        return self.connector_service.get(service_name)

    def remove(self, service_name: str) -> bool:
        return self.connector_service.remove(service_name)

    def exists(self, service_name: str) -> bool:
        return self.connector_service.exists(service_name)

    def list_platforms(self) -> list[str]:
        return self.connector_service.list_services()

    def count(self) -> int:
        return self.connector_service.count()

    def supports_action(
        self,
        service_name: str,
        action: str,
    ) -> bool:
        connector = self.get(service_name)

        if connector is None:
            return False

        return connector.supports(action)
