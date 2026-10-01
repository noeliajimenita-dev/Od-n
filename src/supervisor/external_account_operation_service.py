from typing import Any, Callable

from .external_account_connection_service import (
    ExternalAccountConnectionService,
)
from .external_account_operation import ExternalAccountOperation
from .external_account_operation_repository import (
    ExternalAccountOperationRepository,
)


class ExternalAccountOperationService:
    """Coordinates operations on ready external accounts."""

    def __init__(
        self,
        account_service: ExternalAccountConnectionService | None = None,
        repository: ExternalAccountOperationRepository | None = None,
    ) -> None:
        self.account_service = (
            account_service or ExternalAccountConnectionService()
        )
        self.repository = (
            repository or ExternalAccountOperationRepository()
        )

    def create(
        self,
        operation: ExternalAccountOperation,
    ) -> ExternalAccountOperation:
        account = self.account_service.get(operation.account_id)

        if account is None:
            raise ValueError(
                f"Account not found: {operation.account_id}"
            )

        operation.validate_account(account)
        return self.repository.save(operation)

    def execute(
        self,
        operation_id: str,
        handler: Callable[[ExternalAccountOperation], Any],
    ) -> ExternalAccountOperation:
        operation = self._require_operation(operation_id)

        account = self.account_service.get(operation.account_id)

        if account is None:
            raise ValueError(
                f"Account not found: {operation.account_id}"
            )

        operation.validate_account(account)
        operation.start()
        self.repository.update(operation)

        try:
            result = handler(operation)
            operation.complete(result)
        except Exception as exc:
            operation.fail(str(exc))
            self.repository.update(operation)
            raise

        return self.repository.update(operation)

    def get(
        self,
        operation_id: str,
    ) -> ExternalAccountOperation | None:
        return self.repository.get(operation_id)

    def get_by_account(
        self,
        account_id: str,
    ) -> list[ExternalAccountOperation]:
        return self.repository.list_by_account(account_id)

    def get_pending(self) -> list[ExternalAccountOperation]:
        return self.repository.list_pending()

    def get_completed(self) -> list[ExternalAccountOperation]:
        return self.repository.list_completed()

    def get_failed(self) -> list[ExternalAccountOperation]:
        return self.repository.list_failed()

    def _require_operation(
        self,
        operation_id: str,
    ) -> ExternalAccountOperation:
        operation = self.repository.get(operation_id)

        if operation is None:
            raise ValueError(
                f"Operation not found: {operation_id}"
            )

        return operation
