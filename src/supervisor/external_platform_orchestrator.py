from typing import Any

from .external_account_connection import ExternalAccountConnection
from .external_account_operation import ExternalAccountOperation
from .external_platform_connection_service import (
    ExternalPlatformConnectionService,
)
from .external_platform_connector_service import (
    ExternalPlatformConnectorService,
)
from .external_platform_operation_service import (
    ExternalPlatformOperationService,
)


class ExternalPlatformOrchestrator:
    """Coordinates external platform connections and operations."""

    def __init__(
        self,
        connector_service: ExternalPlatformConnectorService | None = None,
        connection_service: ExternalPlatformConnectionService | None = None,
        operation_service: ExternalPlatformOperationService | None = None,
    ) -> None:
        self.connector_service = (
            connector_service
            or ExternalPlatformConnectorService()
        )

        self.connection_service = (
            connection_service
            or ExternalPlatformConnectionService(
                self.connector_service
            )
        )

        self.operation_service = (
            operation_service
            or ExternalPlatformOperationService(
                self.connector_service
            )
        )

    def connect(
        self,
        account: ExternalAccountConnection,
    ) -> bool:
        return self.connection_service.connect(account)

    def disconnect(
        self,
        account: ExternalAccountConnection,
    ) -> None:
        self.connection_service.disconnect(account)

    def execute(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ) -> Any:
        return self.operation_service.execute(
            operation,
            account,
        )

    def is_supported(self, service_name: str) -> bool:
        return self.connector_service.exists(service_name)

    def supports_action(
        self,
        service_name: str,
        action: str,
    ) -> bool:
        connector = self.connector_service.get(service_name)

        if connector is None:
            return False

        return connector.supports(action)

    def list_platforms(self) -> list[str]:
        return self.connector_service.list_services()
