from datetime import datetime, timezone

from src.telegram.connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from src.telegram.connection_supervisor_command_audit_service import (
    ConnectionCommandAuditService,
)


def create_audit(
    audit_id: str = "audit-1",
    success: bool = True,
) -> ConnectionCommandAudit:
    return ConnectionCommandAudit(
        audit_id=audit_id,
        command="CONNECT",
        bot_name="bot_1",
        success=success,
        message="Resultado de prueba.",
        timestamp=datetime.now(timezone.utc),
    )


def test_service_records_and_gets_audit():
    service = ConnectionCommandAuditService()
    audit = create_audit()

    service.record(audit)

    assert service.count() == 1
    assert service.get(audit.audit_id) is audit


def test_service_returns_all_audits():
    service = ConnectionCommandAuditService()

    first = create_audit("audit-1")
    second = create_audit("audit-2", False)

    service.record(first)
    service.record(second)

    audits = service.get_all()

    assert len(audits) == 2
    assert audits[0] is first
    assert audits[1] is second


def test_service_returns_status():
    service = ConnectionCommandAuditService()

    service.record(create_audit("audit-1", True))
    service.record(create_audit("audit-2", False))

    status = service.get_status()

    assert status.total == 2
    assert status.successful == 1
    assert status.failed == 1


def test_service_builds_report():
    service = ConnectionCommandAuditService()

    service.record(create_audit("audit-1", True))

    report = service.build_report()

    assert "TELEGRAM COMMAND AUDIT" in report
    assert "Total: 1" in report
    assert "Successful: 1" in report
    assert "Failed: 0" in report
