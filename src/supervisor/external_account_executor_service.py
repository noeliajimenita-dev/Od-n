from collections.abc import Callable
from typing import Any

from .external_account_connection import ExternalAccountConnection
from .external_account_executor_repository import (
    ExternalAccountExecutorRepository,
)
from .external_account_operation import ExternalAccountOperation


class ExternalAccountExecutorService:
    """Service layer for external account executors."""

    def __init__(
        self,
        repository: ExternalAccountExecutorRepository | None = None,
    ) -> None:
        self.repository = (
            repository or ExternalAccountExecutorRepository()
        )

    def register_handler(
        self,
        action: str,
        handler: Callable[
            [ExternalAccountOperation, ExternalAccountConnection],
            Any,
        ],
    ) -> None:
        self.repository.register(action, handler)

    def get_handler(
        self,
        action: str,
    ) -> Callable[
        [ExternalAccountOperation, ExternalAccountConnection],
        Any,
    ] | None:
        return self.repository.get(action)

    def supports(self, action: str) -> bool:
        return self.repository.exists(action)

    def execute(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ) -> Any:
        operation.validate_account(account)

        if not account.is_ready:
            raise ValueError(
                f"Account is not ready: {account.account_id}"
            )

        handler = self.repository.get(operation.action)

        if handler is None:
            raise ValueError(
                f"No handler registered for action: "
                f"{operation.action}"
            )

        return handler(operation, account)

    def list_supported_actions(self) -> list[str]:
        return self.repository.list_actions()

    def count_handlers(self) -> int:
        return self.repository.count()
