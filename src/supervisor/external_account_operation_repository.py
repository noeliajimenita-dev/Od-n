from .external_account_operation import ExternalAccountOperation


class ExternalAccountOperationRepository:
    """Repository for external account operations."""

    def __init__(self) -> None:
        self._operations: dict[str, ExternalAccountOperation] = {}

    def save(
        self,
        operation: ExternalAccountOperation,
    ) -> ExternalAccountOperation:
        self._operations[operation.operation_id] = operation
        return operation

    def get(
        self,
        operation_id: str,
    ) -> ExternalAccountOperation | None:
        return self._operations.get(operation_id)

    def exists(self, operation_id: str) -> bool:
        return operation_id in self._operations

    def update(
        self,
        operation: ExternalAccountOperation,
    ) -> ExternalAccountOperation:
        if operation.operation_id not in self._operations:
            raise ValueError(
                f"Operation not found: {operation.operation_id}"
            )

        self._operations[operation.operation_id] = operation
        return operation

    def delete(self, operation_id: str) -> bool:
        if operation_id not in self._operations:
            return False

        del self._operations[operation_id]
        return True

    def list_all(self) -> list[ExternalAccountOperation]:
        return list(self._operations.values())

    def list_by_account(
        self,
        account_id: str,
    ) -> list[ExternalAccountOperation]:
        return [
            operation
            for operation in self._operations.values()
            if operation.account_id == account_id
        ]

    def list_pending(self) -> list[ExternalAccountOperation]:
        return [
            operation
            for operation in self._operations.values()
            if operation.is_pending
        ]

    def list_running(self) -> list[ExternalAccountOperation]:
        return [
            operation
            for operation in self._operations.values()
            if operation.is_running
        ]

    def list_completed(self) -> list[ExternalAccountOperation]:
        return [
            operation
            for operation in self._operations.values()
            if operation.is_completed
        ]

    def list_failed(self) -> list[ExternalAccountOperation]:
        return [
            operation
            for operation in self._operations.values()
            if operation.is_failed
        ]

    def count(self) -> int:
        return len(self._operations)

    def clear(self) -> None:
        self._operations.clear()
