from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class AuthorizationRequest:
    """Representa una solicitud de autorización."""

    action: str
    requester: str
    reason: str
    task_id: str | None = None
    request_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    approved: bool = False
    resolved: bool = False

    def approve(self) -> None:
        """Marca la solicitud como aprobada."""

        self.approved = True
        self.resolved = True

    def deny(self) -> None:
        """Marca la solicitud como rechazada."""

        self.approved = False
        self.resolved = True

    def is_pending(self) -> bool:
        """Indica si la solicitud todavía está pendiente."""

        return not self.resolved
