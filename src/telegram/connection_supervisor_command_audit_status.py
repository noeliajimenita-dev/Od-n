from dataclasses import dataclass

from .connection_supervisor_command_audit_logger import (
    ConnectionCommandAuditLogger,
)


@dataclass(frozen=True)
class ConnectionCommandAuditStatus:
    total: int
    successful: int
    failed: int


def get_connection_command_audit_status(
    logger: ConnectionCommandAuditLogger,
) -> ConnectionCommandAuditStatus:
    entries = logger.get_all()

    successful = sum(1 for entry in entries if entry.success)
    failed = sum(1 for entry in entries if not entry.success)

    return ConnectionCommandAuditStatus(
        total=len(entries),
        successful=successful,
        failed=failed,
    )
