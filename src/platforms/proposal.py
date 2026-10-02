from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Proposal:
    """Propuesta preparada por ODIN para un trabajo."""

    proposal_id: str
    job_id: str
    account_id: str
    message: str
    price: float
    delivery_hours: float
    status: str = "draft"
    authorization_required: bool = True
    authorization_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.proposal_id.strip():
            raise ValueError(
                "proposal_id cannot be empty"
            )

        if not self.job_id.strip():
            raise ValueError(
                "job_id cannot be empty"
            )

        if not self.account_id.strip():
            raise ValueError(
                "account_id cannot be empty"
            )

        if not self.message.strip():
            raise ValueError(
                "message cannot be empty"
            )

        if self.price < 0:
            raise ValueError(
                "price cannot be negative"
            )

        if self.delivery_hours <= 0:
            raise ValueError(
                "delivery_hours must be positive"
            )

    def mark_ready(self) -> None:
        self.status = "ready"

    def mark_authorized(
        self,
        authorization_id: str,
    ) -> None:
        if not authorization_id.strip():
            raise ValueError(
                "authorization_id cannot be empty"
            )

        self.authorization_id = authorization_id
        self.authorization_required = False
        self.status = "authorized"

    def mark_submitted(self) -> None:
        if self.authorization_required:
            raise ValueError(
                "Proposal requires authorization"
            )

        if self.status != "authorized":
            raise ValueError(
                "Proposal must be authorized "
                "before submission"
            )

        self.status = "submitted"

    def mark_rejected(self) -> None:
        self.status = "rejected"

    def mark_withdrawn(self) -> None:
        self.status = "withdrawn"

    def is_ready(self) -> bool:
        return self.status == "ready"

    def is_authorized(self) -> bool:
        return self.status == "authorized"

    def is_submitted(self) -> bool:
        return self.status == "submitted"

    def requires_authorization(self) -> bool:
        return self.authorization_required

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        if not key.strip():
            raise ValueError(
                "metadata key cannot be empty"
            )

        self.metadata[key] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "job_id": self.job_id,
            "account_id": self.account_id,
            "message": self.message,
            "price": self.price,
            "delivery_hours": self.delivery_hours,
            "status": self.status,
            "authorization_required": (
                self.authorization_required
            ),
            "authorization_id": (
                self.authorization_id
            ),
            "metadata": dict(self.metadata),
        }

    def __repr__(self) -> str:
        return (
            "Proposal("
            f"proposal_id={self.proposal_id!r}, "
            f"job_id={self.job_id!r}, "
            f"status={self.status!r}"
            ")"
          )
