from .connection_supervisor_command_execution import (
    ConnectionSupervisorCommandExecution,
)
from .connection_supervisor_command_response_manager import (
    ConnectionSupervisorCommandResponseManager,
)
from .connection_supervisor_command_result import ConnectionCommandResult
from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandResponseIntegration:
    def __init__(
        self,
        execution: ConnectionSupervisorCommandExecution,
        response_manager: ConnectionSupervisorCommandResponseManager,
    ):
        self.execution = execution
        self.response_manager = response_manager

    def execute(
        self,
        request: ConnectionCommandRequest,
    ) -> str:
        result: ConnectionCommandResult | None = self.execution.execute(
            request
        )

        return self.response_manager.process(result)
