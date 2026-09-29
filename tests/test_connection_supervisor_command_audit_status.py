from datetime import datetime, timezone

from src.telegram.connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from src.telegram.connection_supervisor_command_audit_logger import (
    ConnectionCommandAuditLogger,
)
from src.telegram.connection_supervisor_command_audit_status import (
    get_connection_command_audit_status,
)


def create_audit(
    audit_id: str,
    success: bool,
) -> ConnectionCommandAudit:
    return ConnectionCommandAudit(
        audit_id=audit_id,
        command="CONNECT",
        bot_name="bot_1",
        success=success,
        message="Resultado de prueba.",
        timestamp=datetime.now(timezone.utc),
    )


def test_audit_status_counts_successful_and_failed_entries():
    logger = ConnectionCommandAuditLogger()

    logger.record(create_audit("audit-1", True))
    logger.record(create_audit("audit-2", True))
    logger.record(create_audit("audit-3", False))

    status = get_connection_command_audit_status(logger)

    assert status.total == 3
    assert status.successful == 2
    assert status.failed == 1


def test_empty_audit_status():
    logger = ConnectionCommandAuditLogger()

    status = get_connection_command_audit_status(logger)

    assert status.total == 0
    assert status.successful == 0
    assert status.failed == 0
