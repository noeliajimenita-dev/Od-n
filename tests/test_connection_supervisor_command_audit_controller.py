from datetime import datetime, timezone

from src.telegram.connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from src.telegram.connection_supervisor_command_audit_controller import (
    ConnectionCommandAuditController,
)
from src.telegram.connection_supervisor_command_audit_service import (
    ConnectionCommandAuditService,
)


def create_audit(
    audit_id: str = "audit-1",
) -> ConnectionCommandAudit:
    return ConnectionCommandAudit(
        audit_id=audit_id,
        command="CONNECT",
        bot_name="bot_1",
        success=True,
        message="Bot conectado correctamente.",
        timestamp=datetime.now(timezone.utc),
    )


def test_controller_records_audit():
    service = ConnectionCommandAuditService()
    controller = ConnectionCommandAuditController(service)

    audit = create_audit()

    controller.record(audit)

    assert controller.count() == 1
    assert controller.get(audit.audit_id) is audit


def test_controller_returns_all_audits():
    service = ConnectionCommandAuditService()
    controller = ConnectionCommandAuditController(service)

    first = create_audit("audit-1")
    second = create_audit("audit-2")

    controller.record(first)
    controller.record(second)

    audits = controller.get_all()

    assert len(audits) == 2
    assert audits[0] is first
    assert audits[1] is second


def test_controller_returns_status():
    service = ConnectionCommandAuditService()
    controller = ConnectionCommandAuditController(service)

    controller.record(create_audit())

    status = controller.status()

    assert status.total == 1
    assert status.successful == 1
    assert status.failed == 0


def test_controller_generates_report():
    service = ConnectionCommandAuditService()
    controller = ConnectionCommandAuditController(service)

    controller.record(create_audit())

    report = controller.report()

    assert "TELEGRAM COMMAND AUDIT" in report
    assert "Total: 1" in report
