from .connection_supervisor_command_audit_manager import (
    ConnectionSupervisorCommandAuditManager,
)
from .connection_supervisor_commands import ConnectionCommandRequest
from .connection_supervisor_command_result import ConnectionCommandResult


class ConnectionSupervisorCommandDispatcher:
    def __init__(
        self,
        audit_manager: ConnectionSupervisorCommandAuditManager,
    ):
        self.audit_manager = audit_manager

    def dispatch(
        self,
        request: ConnectionCommandRequest,
    ) -> ConnectionCommandResult:
        return self.audit_manager.execute(request)
