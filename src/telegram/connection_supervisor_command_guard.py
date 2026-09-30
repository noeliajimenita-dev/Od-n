from .connection_supervisor_command_security import (
    ConnectionSupervisorCommandSecurity,
)
from .connection_supervisor_command_validation import (
    ConnectionSupervisorCommandValidation,
)
from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandGuard:
    def __init__(
        self,
        validation: ConnectionSupervisorCommandValidation,
        security: ConnectionSupervisorCommandSecurity,
    ):
        self.validation = validation
        self.security = security

    def allow(
        self,
        request: ConnectionCommandRequest,
    ) -> bool:
        if not self.validation.validate(request):
            return False

        return self.security.is_allowed(request)
