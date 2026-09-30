from .connection_supervisor_command_audit_integration import (
    ConnectionSupervisorCommandAuditIntegration,
)
from .connection_supervisor_command_audit_service import (
    ConnectionCommandAuditService,
)
from .connection_supervisor_command_result import (
    ConnectionCommandResult,
)
from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandAuditManager:
    def __init__(
        self,
        integration: ConnectionSupervisorCommandAuditIntegration,
        audit_service: ConnectionCommandAuditService,
    ):
        self.integration = integration
        self.audit_service = audit_service

    def execute(
        self,
        request: ConnectionCommandRequest,
    ) -> ConnectionCommandResult:
        return self.integration.execute(request)

    def get_audit_count(self) -> int:
        return self.audit_service.count()

    def get_audits(self):
        return self.audit_service.get_all()

    def get_status(self):
        return self.audit_service.get_status()

    def get_report(self) -> str:
        return self.audit_service.build_report()
