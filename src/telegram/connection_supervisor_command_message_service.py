from .connection_supervisor_command_message import (
    ConnectionSupervisorCommandMessage,
)
from .connection_supervisor_command_message_factory import (
    ConnectionSupervisorCommandMessageFactory,
)


class ConnectionSupervisorCommandMessageService:
    def __init__(
        self,
        factory: ConnectionSupervisorCommandMessageFactory,
    ):
        self.factory = factory

    def process(
        self,
        raw_text: str,
    ) -> ConnectionSupervisorCommandMessage:
        return self.factory.create(raw_text)

    def is_valid(self, raw_text: str) -> bool:
        message = self.process(raw_text)
        return message.is_valid
