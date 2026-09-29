from datetime import datetime, timezone

from src.telegram.connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from src.telegram.connection_supervisor_command_audit_logger import (
    ConnectionCommandAuditLogger,
)
from src.telegram.connection_supervisor_command_audit_report import (
    build_connection_command_audit_report,
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


def test_audit_report_contains_summary():
    logger = ConnectionCommandAuditLogger()

    logger.record(create_audit("audit-1", True))
    logger.record(create_audit("audit-2", True))
    logger.record(create_audit("audit-3", False))

    report = build_connection_command_audit_report(logger)

    assert "TELEGRAM COMMAND AUDIT" in report
    assert "Total: 3" in report
    assert "Successful: 2" in report
    assert "Failed: 1" in report


def test_empty_audit_report():
    logger = ConnectionCommandAuditLogger()

    report = build_connection_command_audit_report(logger)

    assert "Total: 0" in report
    assert "Successful: 0" in report
    assert "Failed: 0" in report
