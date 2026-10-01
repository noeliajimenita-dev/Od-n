from .external_account_connection import ExternalAccountConnection
from .external_account_executor_service import (
    ExternalAccountExecutorService,
)
from .external_account_operation import ExternalAccountOperation
from .external_account_operation_validator import (
    ExternalAccountOperationValidator,
)


class ExternalAccountOperationController:
    """Coordinates external account operations."""

    def __init__(
        self,
        executor_service: ExternalAccountExecutorService | None = None,
        validator: ExternalAccountOperationValidator | None = None,
    ) -> None:
        self.executor_service = (
            executor_service or ExternalAccountExecutorService()
        )
        self.validator = validator or ExternalAccountOperationValidator(
            self.executor_service
        )

    def validate(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ) -> bool:
        return self.validator.validate(operation, account)

    def execute(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ):
        self.validator.validate(operation, account)

        operation.start()

        try:
            result = self.executor_service.execute(
                operation,
                account,
            )
            operation.complete(result)
            return result
        except Exception as exc:
            operation.fail(str(exc))
            raise

    def supports(self, action: str) -> bool:
        return self.executor_service.supports(action)

    def list_supported_actions(self) -> list[str]:
        return self.executor_service.list_supported_actions()
