from .connection_supervisor_command_message import (
    ConnectionSupervisorCommandMessage,
)
from .connection_supervisor_command_message_controller import (
    ConnectionSupervisorCommandMessageController,
)


class ConnectionSupervisorCommandMessageIntegration:
    def __init__(
        self,
        controller: ConnectionSupervisorCommandMessageController,
    ):
        self.controller = controller

    def receive(
        self,
        raw_text: str,
    ) -> ConnectionSupervisorCommandMessage:
        return self.controller.handle(raw_text)

    def accepts(self, raw_text: str) -> bool:
        return self.controller.is_valid(raw_text)
