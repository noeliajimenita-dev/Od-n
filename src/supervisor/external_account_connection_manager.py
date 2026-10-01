from .external_account_connection import ExternalAccountConnection
from .external_account_connection_controller import (
    ExternalAccountConnectionController,
)
from .external_account_connection_status import (
    ExternalAccountConnectionStatus,
)


class ExternalAccountConnectionManager:
    """Central manager for operational external accounts."""

    def __init__(
        self,
        controller: ExternalAccountConnectionController | None = None,
        status: ExternalAccountConnectionStatus | None = None,
    ) -> None:
        self.controller = (
            controller or ExternalAccountConnectionController()
        )
        self.status = status or ExternalAccountConnectionStatus(
            self.controller.service
        )

    def register(
        self,
        account: ExternalAccountConnection,
    ) -> ExternalAccountConnection:
        return self.controller.register(account)

    def verify(self, account_id: str) -> ExternalAccountConnection:
        return self.controller.verify(account_id)

    def disconnect(self, account_id: str) -> ExternalAccountConnection:
        return self.controller.disconnect(account_id)

    def reconnect(self, account_id: str) -> ExternalAccountConnection:
        return self.controller.reconnect(account_id)

    def get_status(self, account_id: str) -> dict:
        return self.status.get_status(account_id)

    def get_all_statuses(self) -> list[dict]:
        return self.status.get_all_statuses()

    def is_ready(self, account_id: str) -> bool:
        return self.status.get_status(account_id)["ready"]

    def get_ready_accounts(self) -> list[ExternalAccountConnection]:
        return self.controller.get_ready_accounts()
