from typing import Any, Callable

from .external_account_connection import ExternalAccountConnection
from .external_account_operation import ExternalAccountOperation


class ExternalAccountExecutor:
    """Executes authorized operations on ready external accounts."""

    def __init__(
        self,
        handlers: dict[str, Callable[[ExternalAccountOperation, ExternalAccountConnection], Any]]
        | None = None,
    ) -> None:
        self.handlers = handlers or {}

    def register_handler(
        self,
        action: str,
        handler: Callable[
            [ExternalAccountOperation, ExternalAccountConnection],
            Any,
        ],
    ) -> None:
        if not action.strip():
            raise ValueError("action cannot be empty")

        self.handlers[action] = handler

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

        handler = self.handlers.get(operation.action)

        if handler is None:
            raise ValueError(
                f"No handler registered for action: {operation.action}"
            )

        return handler(operation, account)

    def supports(self, action: str) -> bool:
        return action in self.handlers

    def supported_actions(self) -> list[str]:
        return list(self.handlers.keys())
