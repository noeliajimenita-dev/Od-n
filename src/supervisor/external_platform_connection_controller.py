from .external_account_connection import ExternalAccountConnection
from .external_platform_connection_service import (
    ExternalPlatformConnectionService,
)


class ExternalPlatformConnectionController:
    """Controls platform-specific account connections."""

    def __init__(
        self,
        connection_service: ExternalPlatformConnectionService | None = None,
    ) -> None:
        self.connection_service = (
            connection_service
            or ExternalPlatformConnectionService()
        )

    def connect(self, account: ExternalAccountConnection) -> bool:
        if not account.service.strip():
            raise ValueError("Account service cannot be empty")

        if not self.connection_service.is_supported(account.service):
            raise ValueError(
                f"Unsupported platform: {account.service}"
            )

        connected = self.connection_service.connect(account)

        if connected:
            account.verify()

        return connected

    def disconnect(self, account: ExternalAccountConnection) -> None:
        self.connection_service.disconnect(account)
        account.disconnect()

    def is_supported(self, service_name: str) -> bool:
        if not service_name.strip():
            return False

        return self.connection_service.is_supported(service_name)

    def get_connector(self, service_name: str):
        return self.connection_service.get_connector(service_name)
