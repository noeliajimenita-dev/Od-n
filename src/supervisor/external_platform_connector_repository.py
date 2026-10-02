from .external_platform_connector import ExternalPlatformConnector


class ExternalPlatformConnectorRepository:
    """Repository for external platform connectors."""

    def __init__(self) -> None:
        self._connectors: dict[str, ExternalPlatformConnector] = {}

    def register(
        self,
        connector: ExternalPlatformConnector,
    ) -> ExternalPlatformConnector:
        if not connector.service_name.strip():
            raise ValueError("connector service_name cannot be empty")

        self._connectors[connector.service_name] = connector
        return connector

    def get(
        self,
        service_name: str,
    ) -> ExternalPlatformConnector | None:
        return self._connectors.get(service_name)

    def exists(self, service_name: str) -> bool:
        return service_name in self._connectors

    def remove(self, service_name: str) -> bool:
        if service_name not in self._connectors:
            return False

        del self._connectors[service_name]
        return True

    def list_all(self) -> list[ExternalPlatformConnector]:
        return list(self._connectors.values())

    def list_services(self) -> list[str]:
        return list(self._connectors.keys())

    def count(self) -> int:
        return len(self._connectors)

    def clear(self) -> None:
        self._connectors.clear()
