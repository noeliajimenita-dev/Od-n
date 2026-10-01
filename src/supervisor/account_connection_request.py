from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AccountConnectionRequest:
    """Represents a request to connect an external account."""

    request_id: str
    service: str
    username: str
    status: str = "pending"
    requires_user_action: bool = True
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id or not self.request_id.strip():
            raise ValueError("Request ID cannot be empty")

        if not self.service or not self.service.strip():
            raise ValueError("Service cannot be empty")

        if not self.username or not self.username.strip():
            raise ValueError("Username cannot be empty")

    def mark_ready(self) -> None:
        self.status = "ready"
        self.requires_user_action = False

    def mark_connected(self) -> None:
        self.status = "connected"
        self.requires_user_action = False

    def mark_cancelled(self) -> None:
        self.status = "cancelled"
        self.requires_user_action = False

    def request_user_action(self) -> None:
        self.status = "waiting_for_user"
        self.requires_user_action = True

    @property
    def is_pending(self) -> bool:
        return self.status == "pending"

    @property
    def is_connected(self) -> bool:
        return self.status == "connected"

    @property
    def needs_user_action(self) -> bool:
        return self.requires_user_action

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "service": self.service,
            "username": self.username,
            "status": self.status,
            "requires_user_action": self.requires_user_action,
            "created_at": self.created_at.isoformat(),
            "metadata": dict(self.metadata),
        }
