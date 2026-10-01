from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExternalAccountConnection:
    """Represents the operational state of an external account."""

    account_id: str
    service: str
    username: str
    credential_ref: str
    status: str = "connected"
    verified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.account_id.strip():
            raise ValueError("account_id cannot be empty")

        if not self.service.strip():
            raise ValueError("service cannot be empty")

        if not self.username.strip():
            raise ValueError("username cannot be empty")

        if not self.credential_ref.strip():
            raise ValueError("credential_ref cannot be empty")

    def verify(self) -> None:
        if self.status != "connected":
            raise ValueError(
                "Only connected accounts can be verified"
            )

        self.verified = True

    def disconnect(self) -> None:
        self.status = "disconnected"
        self.verified = False

    def reconnect(self) -> None:
        self.status = "connected"

    @property
    def is_connected(self) -> bool:
        return self.status == "connected"

    @property
    def is_ready(self) -> bool:
        return self.is_connected and self.verified

    def set_metadata(self, key: str, value: Any) -> None:
        if not key.strip():
            raise ValueError("metadata key cannot be empty")

        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "service": self.service,
            "username": self.username,
            "credential_ref": self.credential_ref,
            "status": self.status,
            "verified": self.verified,
            "metadata": dict(self.metadata),
      }
