from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ConnectedAccount:
    """Represents an external account connected securely to ODIN."""

    account_id: str
    service: str
    username: str
    credential_ref: str
    status: str = "connected"
    verification_required: bool = False
    verification_type: str | None = None
    connected_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.account_id or not self.account_id.strip():
            raise ValueError("Account ID cannot be empty")

        if not self.service or not self.service.strip():
            raise ValueError("Service cannot be empty")

        if not self.username or not self.username.strip():
            raise ValueError("Username cannot be empty")

        if not self.credential_ref or not self.credential_ref.strip():
            raise ValueError("Credential reference cannot be empty")

    def mark_connected(self) -> None:
        self.status = "connected"
        self.verification_required = False
        self.verification_type = None

    def mark_disconnected(self) -> None:
        self.status = "disconnected"

    def request_verification(self, verification_type: str) -> None:
        if not verification_type or not verification_type.strip():
            raise ValueError("Verification type cannot be empty")

        self.status = "verification_required"
        self.verification_required = True
        self.verification_type = verification_type

    def is_connected(self) -> bool:
        return self.status == "connected"

    def needs_verification(self) -> bool:
        return self.verification_required

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "service": self.service,
            "username": self.username,
            "credential_ref": self.credential_ref,
            "status": self.status,
            "verification_required": self.verification_required,
            "verification_type": self.verification_type,
            "connected_at": self.connected_at.isoformat(),
            "metadata": dict(self.metadata),
        }
