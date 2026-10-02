from typing import Any

from .external_account_connection import ExternalAccountConnection
from .external_account_operation import ExternalAccountOperation
from .external_platform_connector_service import (
    ExternalPlatformConnectorService,
)


class ExternalPlatformOperationService:
    """Executes operations through platform-specific connectors."""

    def __init__(
        self,
        connector_service: ExternalPlatformConnectorService | None = None,
    ) -> None:
        self.connector_service = (
            connector_service
            or ExternalPlatformConnectorService()
        )

    def execute(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ) -> Any:
        if operation.account_id != account.account_id:
            raise ValueError(
                "Operation account does not match connection"
            )

        if not account.is_ready:
            raise ValueError(
                f"Account is not ready: {account.account_id}"
            )

        connector = self.connector_service.get_for_service(
            account.service
        )

        if not connector.supports(operation.action):
            raise ValueError(
                f"Unsupported action '{operation.action}' "
                f"for service '{account.service}'"
            )

        return connector.execute(operation, account)

    def supports(
        self,
        service_name: str,
        action: str,
    ) -> bool:
        connector = self.connector_service.get(service_name)

        if connector is None:
            return False

        return connector.supports(action)

    def list_services(self) -> list[str]:
        return self.connector_service.list_services()
