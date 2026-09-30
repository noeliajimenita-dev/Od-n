from .connection_supervisor_command_result_handler import (
    ConnectionSupervisorCommandResultHandler,
)
from .connection_supervisor_command_result import ConnectionCommandResult


class ConnectionSupervisorCommandResponse:
    def __init__(
        self,
        result_handler: ConnectionSupervisorCommandResultHandler,
    ):
        self.result_handler = result_handler

    def build(
        self,
        result: ConnectionCommandResult | None,
    ) -> str:
        return self.result_handler.handle(result)
