from .external_platform_connector import ExternalPlatformConnector
from .external_platform_connector_repository import (
    ExternalPlatformConnectorRepository,
)


class ExternalPlatformConnectorService:
    """Service layer for external platform connectors."""

    def __init__(
        self,
        repository: ExternalPlatformConnectorRepository | None = None,
    ) -> None:
        self.repository = (
            repository or ExternalPlatformConnectorRepository()
        )

    def register(
        self,
        connector: ExternalPlatformConnector,
    ) -> ExternalPlatformConnector:
        return self.repository.register(connector)

    def get(
        self,
        service_name: str,
    ) -> ExternalPlatformConnector | None:
        return self.repository.get(service_name)

    def exists(self, service_name: str) -> bool:
        return self.repository.exists(service_name)

    def remove(self, service_name: str) -> bool:
        return self.repository.remove(service_name)

    def list_connectors(self) -> list[ExternalPlatformConnector]:
        return self.repository.list_all()

    def list_services(self) -> list[str]:
        return self.repository.list_services()

    def count(self) -> int:
        return self.repository.count()

    def get_for_service(
        self,
        service_name: str,
    ) -> ExternalPlatformConnector:
        connector = self.repository.get(service_name)

        if connector is None:
            raise ValueError(
                f"No connector registered for service: {service_name}"
            )

        return connector
