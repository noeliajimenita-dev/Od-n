from .connection_supervisor_command_audit_logger import (
    ConnectionCommandAuditLogger,
)
from .connection_supervisor_command_audit_status import (
    get_connection_command_audit_status,
)


def build_connection_command_audit_report(
    logger: ConnectionCommandAuditLogger,
) -> str:
    status = get_connection_command_audit_status(logger)

    return (
        "TELEGRAM COMMAND AUDIT\n"
        f"Total: {status.total}\n"
        f"Successful: {status.successful}\n"
        f"Failed: {status.failed}"
    )
