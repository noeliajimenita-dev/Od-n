from .connection_supervisor_command_message import (
    ConnectionSupervisorCommandMessage,
)
from .connection_supervisor_command_parser import (
    ConnectionSupervisorCommandParser,
)


class ConnectionSupervisorCommandMessageFactory:
    def __init__(self, parser: ConnectionSupervisorCommandParser):
        self.parser = parser

    def create(self, raw_text: str) -> ConnectionSupervisorCommandMessage:
        command = self.parser.parse(raw_text)

        return ConnectionSupervisorCommandMessage(
            raw_text=raw_text,
            command=command,
        )
