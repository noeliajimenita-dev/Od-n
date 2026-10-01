from .external_account_connection import ExternalAccountConnection
from .external_account_operation import ExternalAccountOperation
from .external_account_operation_controller import (
    ExternalAccountOperationController,
)
from .external_account_operation_result import (
    ExternalAccountOperationResult,
)
from .external_account_operation_result_service import (
    ExternalAccountOperationResultService,
)


class ExternalAccountOperationOrchestrator:
    """Coordinates execution and result recording."""

    def __init__(
        self,
        controller: ExternalAccountOperationController | None = None,
        result_service: ExternalAccountOperationResultService | None = None,
    ) -> None:
        self.controller = (
            controller or ExternalAccountOperationController()
        )
        self.result_service = (
            result_service or ExternalAccountOperationResultService()
        )

    def execute(
        self,
        operation: ExternalAccountOperation,
        account: ExternalAccountConnection,
    ) -> ExternalAccountOperationResult:
        try:
            result = self.controller.execute(
                operation,
                account,
            )

            return self.result_service.record_success(
                operation_id=operation.operation_id,
                output=result,
            )

        except Exception as exc:
            return self.result_service.record_failure(
                operation_id=operation.operation_id,
                error=str(exc),
            )

    def get_result(
        self,
        operation_id: str,
    ) -> ExternalAccountOperationResult | None:
        return self.result_service.get(operation_id)

    def summary(self) -> dict[str, int]:
        return self.result_service.summary()
