from .connection_supervisor_command_response_integration import (
    ConnectionSupervisorCommandResponseIntegration,
)
from .connection_supervisor_commands import ConnectionCommandRequest


class ConnectionSupervisorCommandResponseController:
    def __init__(
        self,
        integration: ConnectionSupervisorCommandResponseIntegration,
    ):
        self.integration = integration

    def handle(
        self,
        request: ConnectionCommandRequest,
    ) -> str:
        return self.integration.execute(request)
