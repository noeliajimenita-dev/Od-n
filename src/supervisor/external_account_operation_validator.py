from .external_account_connection import ExternalAccountConnection
from .external_account_executor_service import (
    ExternalAccountExecutorService,
)
from .external_account_operation import ExternalAccountOperation


class ExternalAccountOperationValidator:
    """Validates operations before external execution."""

    def __init__(
        self,
        executor_service: ExternalAccountExecutorService | None = None,
    ) -> None:
        self.executor_service = (
            executor_service or ExternalAccountExecutorService()
        )

    def validate(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ) -> bool:
        if not operation.operation_id.strip():
            raise ValueError("operation_id cannot be empty")

        if not operation.action.strip():
            raise ValueError("action cannot be empty")

        operation.validate_account(account)

        if not account.is_ready:
            raise ValueError(
                f"Account is not ready: {account.account_id}"
            )

        if not self.executor_service.supports(operation.action):
            raise ValueError(
                f"Unsupported external action: {operation.action}"
            )

        return True

    def is_valid(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ) -> bool:
        try:
            self.validate(operation, account)
            return True
        except ValueError:
            return False
