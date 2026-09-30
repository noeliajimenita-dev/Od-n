from .connection_supervisor_command_access import (
    ConnectionSupervisorCommandAccess,
)
from .connection_supervisor_command_dispatcher import (
    ConnectionSupervisorCommandDispatcher,
)
from .connection_supervisor_command_result import ConnectionCommandResult
from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandExecution:
    def __init__(
        self,
        access: ConnectionSupervisorCommandAccess,
        dispatcher: ConnectionSupervisorCommandDispatcher,
    ):
        self.access = access
        self.dispatcher = dispatcher

    def execute(
        self,
        request: ConnectionCommandRequest,
    ) -> ConnectionCommandResult | None:
        if not self.access.can_execute(request):
            return None

        return self.dispatcher.dispatch(request)
