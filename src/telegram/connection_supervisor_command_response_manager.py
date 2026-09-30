from .connection_supervisor_command_response_service import (
    ConnectionSupervisorCommandResponseService,
)
from .connection_supervisor_command_result import ConnectionCommandResult


class ConnectionSupervisorCommandResponseManager:
    def __init__(
        self,
        response_service: ConnectionSupervisorCommandResponseService,
    ):
        self.response_service = response_service

    def process(
        self,
        result: ConnectionCommandResult | None,
    ) -> str:
        return self.response_service.handle(result)
