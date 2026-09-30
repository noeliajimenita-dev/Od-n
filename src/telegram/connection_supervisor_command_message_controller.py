from .connection_supervisor_command_message import (
    ConnectionSupervisorCommandMessage,
)
from .connection_supervisor_command_message_service import (
    ConnectionSupervisorCommandMessageService,
)


class ConnectionSupervisorCommandMessageController:
    def __init__(
        self,
        service: ConnectionSupervisorCommandMessageService,
    ):
        self.service = service

    def handle(
        self,
        raw_text: str,
    ) -> ConnectionSupervisorCommandMessage:
        return self.service.process(raw_text)

    def is_valid(self, raw_text: str) -> bool:
        return self.service.is_valid(raw_text)
