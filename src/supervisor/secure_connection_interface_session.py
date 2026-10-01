from dataclasses import dataclass, field
from typing import Any


@dataclass
class SecureConnectionInterfaceSession:
    session_id: str
    request_id: str
    interface_token: str
    status: str = "active"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.session_id.strip():
            raise ValueError("session_id cannot be empty")

        if not self.request_id.strip():
            raise ValueError("request_id cannot be empty")

        if not self.interface_token.strip():
            raise ValueError("interface_token cannot be empty")

    def complete(self) -> None:
        if self.status != "active":
            raise ValueError("Only active sessions can be completed")

        self.status = "completed"

    def cancel(self) -> None:
        if self.status == "completed":
            raise ValueError("Completed sessions cannot be cancelled")

        self.status = "cancelled"

    def expire(self) -> None:
        if self.status == "completed":
            raise ValueError("Completed sessions cannot expire")

        self.status = "expired"

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def is_completed(self) -> bool:
        return self.status == "completed"

    @property
    def is_cancelled(self) -> bool:
        return self.status == "cancelled"

    @property
    def is_expired(self) -> bool:
        return self.status == "expired"

    def set_metadata(self, key: str, value: Any) -> None:
        if not key.strip():
            raise ValueError("metadata key cannot be empty")

        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "request_id": self.request_id,
            "interface_token": self.interface_token,
            "status": self.status,
            "metadata": dict(self.metadata),
      }
