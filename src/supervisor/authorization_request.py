from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AuthorizationRequest:
    """Represents a sensitive action requiring user authorization."""

    request_id: str
    action: str
    reason: str
    purpose: str
    time_limit_minutes: int | None = None
    status: str = "pending"
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id or not self.request_id.strip():
            raise ValueError("Request ID cannot be empty")

        if not self.action or not self.action.strip():
            raise ValueError("Action cannot be empty")

        if not self.reason or not self.reason.strip():
            raise ValueError("Reason cannot be empty")

        if not self.purpose or not self.purpose.strip():
            raise ValueError("Purpose cannot be empty")

        if (
            self.time_limit_minutes is not None
            and self.time_limit_minutes <= 0
        ):
            raise ValueError("Time limit must be greater than zero")

    def approve(self) -> None:
        self.status = "approved"

    def reject(self) -> None:
        self.status = "rejected"

    def expire(self) -> None:
        self.status = "expired"

    @property
    def is_pending(self) -> bool:
        return self.status == "pending"

    @property
    def is_approved(self) -> bool:
        return self.status == "approved"

    @property
    def is_rejected(self) -> bool:
        return self.status == "rejected"

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "action": self.action,
            "reason": self.reason,
            "purpose": self.purpose,
            "time_limit_minutes": self.time_limit_minutes,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "metadata": dict(self.metadata),
          }
