from typing import Any

from .external_account_operation_result import (
    ExternalAccountOperationResult,
)
from .external_account_operation_result_repository import (
    ExternalAccountOperationResultRepository,
)


class ExternalAccountOperationResultService:
    """Service layer for external operation results."""

    def __init__(
        self,
        repository: ExternalAccountOperationResultRepository | None = None,
    ) -> None:
        self.repository = (
            repository
            or ExternalAccountOperationResultRepository()
        )

    def record_success(
        self,
        operation_id: str,
        output: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> ExternalAccountOperationResult:
        result = ExternalAccountOperationResult(
            operation_id=operation_id,
            status="completed",
            output=output,
            metadata=metadata or {},
        )
        return self.repository.save(result)

    def record_failure(
        self,
        operation_id: str,
        error: str,
        metadata: dict[str, Any] | None = None,
    ) -> ExternalAccountOperationResult:
        if not error.strip():
            raise ValueError("error cannot be empty")

        result = ExternalAccountOperationResult(
            operation_id=operation_id,
            status="failed",
            error=error,
            metadata=metadata or {},
        )
        return self.repository.save(result)

    def get(
        self,
        operation_id: str,
    ) -> ExternalAccountOperationResult | None:
        return self.repository.get(operation_id)

    def has_result(self, operation_id: str) -> bool:
        return self.repository.exists(operation_id)

    def get_successful(
        self,
    ) -> list[ExternalAccountOperationResult]:
        return self.repository.list_successful()

    def get_failed(
        self,
    ) -> list[ExternalAccountOperationResult]:
        return self.repository.list_failed()

    def summary(self) -> dict[str, int]:
        return {
            "total": self.repository.count(),
            "successful": self.repository.count_successful(),
            "failed": self.repository.count_failed(),
      }
