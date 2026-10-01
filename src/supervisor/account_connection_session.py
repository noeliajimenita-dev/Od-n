from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AccountConnectionSession:
    """Represents a temporary account connection session."""

    session_id: str
    request_id: str
    service: str
    status: str = "waiting_for_user"
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.session_id or not self.session_id.strip():
            raise ValueError("Session ID cannot be empty")

        if not self.request_id or not self.request_id.strip():
            raise ValueError("Request ID cannot be empty")

        if not self.service or not self.service.strip():
            raise ValueError("Service cannot be empty")

    def mark_ready(self) -> None:
        self.status = "ready"

    def mark_completed(self) -> None:
        self.status = "completed"

    def mark_cancelled(self) -> None:
        self.status = "cancelled"

    def mark_waiting_for_user(self) -> None:
        self.status = "waiting_for_user"

    @property
    def is_waiting_for_user(self) -> bool:
        return self.status == "waiting_for_user"

    @property
    def is_completed(self) -> bool:
        return self.status == "completed"

    @property
    def is_cancelled(self) -> bool:
        return self.status == "cancelled"

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "request_id": self.request_id,
            "service": self.service,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "metadata": dict(self.metadata),
      }
