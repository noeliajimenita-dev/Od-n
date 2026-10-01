from .external_account_operation_result_service import (
    ExternalAccountOperationResultService,
)


class ExternalAccountOperationStatus:
    """Provides consolidated status for external operations."""

    def __init__(
        self,
        result_service: ExternalAccountOperationResultService | None = None,
    ) -> None:
        self.result_service = (
            result_service
            or ExternalAccountOperationResultService()
        )

    def get_status(self, operation_id: str) -> dict:
        result = self.result_service.get(operation_id)

        if result is None:
            return {
                "operation_id": operation_id,
                "exists": False,
                "status": "unknown",
                "success": False,
                "failed": False,
            }

        return {
            "operation_id": result.operation_id,
            "exists": True,
            "status": result.status,
            "success": result.success,
            "failed": result.failed,
            "error": result.error,
        }

    def get_summary(self) -> dict[str, int]:
        return self.result_service.summary()

    def has_result(self, operation_id: str) -> bool:
        return self.result_service.has_result(operation_id)

    def is_successful(self, operation_id: str) -> bool:
        result = self.result_service.get(operation_id)
        return result is not None and result.success

    def is_failed(self, operation_id: str) -> bool:
        result = self.result_service.get(operation_id)
        return result is not None and result.failed
