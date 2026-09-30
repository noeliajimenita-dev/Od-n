from datetime import datetime, timezone

from src.telegram.connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from src.telegram.connection_supervisor_command_audit_integration import (
    ConnectionSupervisorCommandAuditIntegration,
)
from src.telegram.connection_supervisor_command_audit_manager import (
    ConnectionSupervisorCommandAuditManager,
)
from src.telegram.connection_supervisor_command_audit_service import (
    ConnectionCommandAuditService,
)
from src.telegram.connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from src.telegram.connection_supervisor_commands import (
    ConnectionCommandRequest,
)


class FakeIntegration:
    def __init__(self):
        self.executed_requests = []

    def execute(
        self,
        request: ConnectionCommandRequest,
    ) -> ConnectionCommandResult:
        self.executed_requests.append(request)

        return ConnectionCommandResult.ok(
            message="Comando ejecutado correctamente.",
            bot_name=request.bot_name,
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


def test_manager_executes_command():
    integration = FakeIntegration()
    audit_service = ConnectionCommandAuditService()

    manager = ConnectionSupervisorCommandAuditManager(
        integration=integration,
        audit_service=audit_service,
    )

    request = ConnectionCommandRequest(
        command="CONNECT",
        bot_name="bot_1",
    )

    result = manager.execute(request)

    assert result.success is True
    assert len(integration.executed_requests) == 1
    assert integration.executed_requests[0] is request


def test_manager_returns_audit_count():
    integration = FakeIntegration()
    audit_service = ConnectionCommandAuditService()

    audit_service.record(create_audit())

    manager = ConnectionSupervisorCommandAuditManager(
        integration=integration,
        audit_service=audit_service,
    )

    assert manager.get_audit_count() == 1


def test_manager_returns_audits():
    integration = FakeIntegration()
    audit_service = ConnectionCommandAuditService()

    audit = create_audit()
    audit_service.record(audit)

    manager = ConnectionSupervisorCommandAuditManager(
        integration=integration,
        audit_service=audit_service,
    )

    audits = manager.get_audits()

    assert len(audits) == 1
    assert audits[0] is audit


def test_manager_returns_status():
    integration = FakeIntegration()
    audit_service = ConnectionCommandAuditService()

    audit_service.record(create_audit("audit-1", True))
    audit_service.record(create_audit("audit-2", False))

    manager = ConnectionSupervisorCommandAuditManager(
        integration=integration,
        audit_service=audit_service,
    )

    status = manager.get_status()

    assert status.total == 2
    assert status.successful == 1
    assert status.failed == 1


def test_manager_generates_report():
    integration = FakeIntegration()
    audit_service = ConnectionCommandAuditService()

    audit_service.record(create_audit())

    manager = ConnectionSupervisorCommandAuditManager(
        integration=integration,
        audit_service=audit_service,
    )

    report = manager.get_report()

    assert "TELEGRAM COMMAND AUDIT" in report
    assert "Total: 1" in report
    assert "Successful: 1" in report
    assert "Failed: 0" in report
