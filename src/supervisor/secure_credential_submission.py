from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SecureCredentialSubmission:
    request_id: str
    session_id: str
    credential_ref: str
    status: str = "submitted"
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id cannot be empty")

        if not self.session_id.strip():
            raise ValueError("session_id cannot be empty")

        if not self.credential_ref.strip():
            raise ValueError("credential_ref cannot be empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "session_id": self.session_id,
            "credential_ref": self.credential_ref,
            "status": self.status,
            "metadata": dict(self.metadata or {}),
        }
