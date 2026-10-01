from .external_account_operation_result import (
    ExternalAccountOperationResult,
)


class ExternalAccountOperationResultRepository:
    """Repository for external account operation results."""

    def __init__(self) -> None:
        self._results: dict[str, ExternalAccountOperationResult] = {}

    def save(
        self,
        result: ExternalAccountOperationResult,
    ) -> ExternalAccountOperationResult:
        self._results[result.operation_id] = result
        return result

    def get(
        self,
        operation_id: str,
    ) -> ExternalAccountOperationResult | None:
        return self._results.get(operation_id)

    def exists(self, operation_id: str) -> bool:
        return operation_id in self._results

    def delete(self, operation_id: str) -> bool:
        if operation_id not in self._results:
            return False

        del self._results[operation_id]
        return True

    def list_all(self) -> list[ExternalAccountOperationResult]:
        return list(self._results.values())

    def list_successful(self) -> list[ExternalAccountOperationResult]:
        return [
            result
            for result in self._results.values()
            if result.success
        ]

    def list_failed(self) -> list[ExternalAccountOperationResult]:
        return [
            result
            for result in self._results.values()
            if result.failed
        ]

    def count(self) -> int:
        return len(self._results)

    def count_successful(self) -> int:
        return len(self.list_successful())

    def count_failed(self) -> int:
        return len(self.list_failed())

    def clear(self) -> None:
        self._results.clear()
