from .connection_supervisor_command_dispatcher import (
    ConnectionSupervisorCommandDispatcher,
)
from .connection_supervisor_command_result import ConnectionCommandResult
from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandPipeline:
    def __init__(
        self,
        dispatcher: ConnectionSupervisorCommandDispatcher,
    ):
        self.dispatcher = dispatcher

    def process(
        self,
        request: ConnectionCommandRequest,
    ) -> ConnectionCommandResult:
        return self.dispatcher.dispatch(request)
