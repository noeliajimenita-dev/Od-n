from dataclasses import dataclass, field
from typing import Any

from .external_account_connection import ExternalAccountConnection


@dataclass
class ExternalAccountOperation:
    """Represents an operation requested for an external account."""

    operation_id: str
    account_id: str
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    result: Any = None
    error: str | None = None

    def __post_init__(self) -> None:
        if not self.operation_id.strip():
            raise ValueError("operation_id cannot be empty")

        if not self.account_id.strip():
            raise ValueError("account_id cannot be empty")

        if not self.action.strip():
            raise ValueError("action cannot be empty")

    def validate_account(
        self,
        account: ExternalAccountConnection,
    ) -> None:
        if account.account_id != self.account_id:
            raise ValueError("Account does not match operation")

        if not account.is_ready:
            raise ValueError(
                f"Account is not ready: {self.account_id}"
            )

    def start(self) -> None:
        if self.status != "pending":
            raise ValueError(
                "Only pending operations can be started"
            )
        self.status = "running"

    def complete(self, result: Any = None) -> None:
        self.status = "completed"
        self.result = result

    def fail(self, error: str) -> None:
        if not error.strip():
            raise ValueError("error cannot be empty")

        self.status = "failed"
        self.error = error

    @property
    def is_pending(self) -> bool:
        return self.status == "pending"

    @property
    def is_running(self) -> bool:
        return self.status == "running"

    @property
    def is_completed(self) -> bool:
        return self.status == "completed"

    @property
    def is_failed(self) -> bool:
        return self.status == "failed"

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "account_id": self.account_id,
            "action": self.action,
            "parameters": dict(self.parameters),
            "status": self.status,
            "result": self.result,
            "error": self.error,
  }
