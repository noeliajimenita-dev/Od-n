from .connection_supervisor_commands import (
    ConnectionCommand,
    ConnectionCommandRequest,
)
from .connection_supervisor_controller import (
    TelegramConnectionSupervisorController,
)


class TelegramConnectionSupervisorCommandHandler:
    def __init__(
        self,
        controller: TelegramConnectionSupervisorController,
    ):
        self.controller = controller

    def handle(self, request: ConnectionCommandRequest) -> str:
        if request.requires_bot() and not request.bot_name:
            raise ValueError("Este comando requiere un bot específico.")

        if request.command == ConnectionCommand.CONNECT:
            self.controller.connect_bot(request.bot_name)
            return f"Bot conectado: {request.bot_name}"

        if request.command == ConnectionCommand.DISCONNECT:
            self.controller.disconnect_bot(request.bot_name)
            return f"Bot desconectado: {request.bot_name}"

        if request.command == ConnectionCommand.RECOVER:
            self.controller.recover_bot(request.bot_name)
            return f"Bot recuperado: {request.bot_name}"

        if request.command == ConnectionCommand.STATUS:
            connected = self.controller.get_connected_bots()
            disconnected = self.controller.get_disconnected_bots()

            return (
                f"Conectados: {len(connected)} | "
                f"Desconectados: {len(disconnected)}"
            )

        raise ValueError(f"Comando no soportado: {request.command}")
