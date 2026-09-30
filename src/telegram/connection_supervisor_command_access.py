from .connection_supervisor_command_guard import (
    ConnectionSupervisorCommandGuard,
)
from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandAccess:
    def __init__(
        self,
        guard: ConnectionSupervisorCommandGuard,
    ):
        self.guard = guard

    def can_execute(
        self,
        request: ConnectionCommandRequest,
    ) -> bool:
        return self.guard.allow(request)
