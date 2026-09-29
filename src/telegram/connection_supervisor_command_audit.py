from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from .connection_supervisor_command_result import ConnectionCommandResult
from .connection_supervisor_commands import ConnectionCommandRequest


@dataclass(frozen=True)
class ConnectionCommandAudit:
    audit_id: str
    command: str
    bot_name: str | None
    success: bool
    message: str
    timestamp: datetime

    @classmethod
    def from_result(
        cls,
        request: ConnectionCommandRequest,
        result: ConnectionCommandResult,
    ) -> "ConnectionCommandAudit":
        return cls(
            audit_id=str(uuid4()),
            command=request.command.value,
            bot_name=request.bot_name,
            success=result.success,
            message=result.message,
            timestamp=datetime.now(timezone.utc),
        )
