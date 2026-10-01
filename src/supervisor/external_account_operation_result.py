from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExternalAccountOperationResult:
    """Represents the result of an external account operation."""

    operation_id: str
    status: str
    output: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.operation_id.strip():
            raise ValueError("operation_id cannot be empty")

        if not self.status.strip():
            raise ValueError("status cannot be empty")

    @property
    def success(self) -> bool:
        return self.status == "completed" and self.error is None

    @property
    def failed(self) -> bool:
        return self.status == "failed"

    def add_metadata(self, key: str, value: Any) -> None:
        if not key.strip():
            raise ValueError("metadata key cannot be empty")

        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "status": self.status,
            "output": self.output,
            "error": self.error,
            "metadata": dict(self.metadata),
        }
