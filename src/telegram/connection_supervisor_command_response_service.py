from .connection_supervisor_command_response import (
    ConnectionSupervisorCommandResponse,
)
from .connection_supervisor_command_response_sender import (
    ConnectionSupervisorCommandResponseSender,
)
from .connection_supervisor_command_result import ConnectionCommandResult


class ConnectionSupervisorCommandResponseService:
    def __init__(
        self,
        response: ConnectionSupervisorCommandResponse,
        sender: ConnectionSupervisorCommandResponseSender,
    ):
        self.response = response
        self.sender = sender

    def handle(
        self,
        result: ConnectionCommandResult | None,
    ) -> str:
        output = self.response.build(result)

        self.sender.send(output)

        return output
