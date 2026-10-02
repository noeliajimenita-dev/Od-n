from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlatformAccount:
    """Cuenta externa que ODIN puede utilizar operativamente."""

    account_id: str
    platform: str
    username: str
    credential_ref: str
    status: str = "connected"
    verified: bool = False
    capabilities: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.account_id.strip():
            raise ValueError("account_id cannot be empty")

        if not self.platform.strip():
            raise ValueError("platform cannot be empty")

        if not self.username.strip():
            raise ValueError("username cannot be empty")

        if not self.credential_ref.strip():
            raise ValueError(
                "credential_ref cannot be empty"
            )

    def connect(self) -> None:
        self.status = "connected"

    def disconnect(self) -> None:
        self.status = "disconnected"

    def verify(self) -> None:
        self.verified = True

    def unverify(self) -> None:
        self.verified = False

    def add_capability(self, capability: str) -> None:
        capability = capability.strip()

        if not capability:
            raise ValueError(
                "capability cannot be empty"
            )

        self.capabilities.add(capability)

    def remove_capability(self, capability: str) -> bool:
        capability = capability.strip()

        if capability not in self.capabilities:
            return False

        self.capabilities.remove(capability)
        return True

    def supports(self, capability: str) -> bool:
        return capability.strip() in self.capabilities

    def is_connected(self) -> bool:
        return self.status == "connected"

    def is_ready(self) -> bool:
        return self.is_connected() and self.verified

    def set_metadata(self, key: str, value: Any) -> None:
        if not key.strip():
            raise ValueError("metadata key cannot be empty")

        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "account_id": self.account_id,
            "platform": self.platform,
            "username": self.username,
            "credential_ref": self.credential_ref,
            "status": self.status,
            "verified": self.verified,
            "capabilities": sorted(self.capabilities),
            "metadata": dict(self.metadata),
        }

    def safe_dict(self) -> dict[str, Any]:
        """Representación segura sin contraseña ni secretos."""
        return self.to_dict()

    def __repr__(self) -> str:
        return (
            "PlatformAccount("
            f"account_id={self.account_id!r}, "
            f"platform={self.platform!r}, "
            f"status={self.status!r}, "
            f"verified={self.verified}"
            ")"
          )
