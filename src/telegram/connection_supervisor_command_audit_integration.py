from .connection_supervisor_command_audit import (
    ConnectionCommandAudit,
)
from .connection_supervisor_command_audit_service import (
    ConnectionCommandAuditService,
)
from .connection_supervisor_command_executor import (
    TelegramConnectionSupervisorCommandExecutor,
)
from .connection_supervisor_commands import (
    ConnectionCommandRequest,
)
from .connection_supervisor_command_result import (
    ConnectionCommandResult,
)


class ConnectionSupervisorCommandAuditIntegration:
    def __init__(
        self,
        executor: TelegramConnectionSupervisorCommandExecutor,
        audit_service: ConnectionCommandAuditService,
    ):
        self.executor = executor
        self.audit_service = audit_service

    def execute(
        self,
        request: ConnectionCommandRequest,
    ) -> ConnectionCommandResult:
        result = self.executor.execute(request)

        audit = ConnectionCommandAudit.from_result(
            request,
            result,
        )

        self.audit_service.record(audit)

        return result
