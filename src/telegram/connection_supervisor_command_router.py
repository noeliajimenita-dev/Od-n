from .connection_supervisor_command_handler import (
    TelegramConnectionSupervisorCommandHandler,
)
from .connection_supervisor_commands import ConnectionCommandRequest


class TelegramConnectionSupervisorCommandRouter:
    def __init__(
        self,
        handler: TelegramConnectionSupervisorCommandHandler,
    ):
        self.handler = handler

    def route(self, request: ConnectionCommandRequest) -> str:
        return self.handler.handle(request)
