from .connection_supervisor_command_result import ConnectionCommandResult
from .connection_supervisor_commands import (
    ConnectionCommand,
    ConnectionCommandRequest,
)
from .connection_supervisor_controller import (
    TelegramConnectionSupervisorController,
)


class TelegramConnectionSupervisorCommandExecutor:
    def __init__(
        self,
        controller: TelegramConnectionSupervisorController,
    ):
        self.controller = controller

    def execute(
        self,
        request: ConnectionCommandRequest,
    ) -> ConnectionCommandResult:
        try:
            if request.requires_bot() and not request.bot_name:
                return ConnectionCommandResult.error(
                    "Este comando requiere un bot específico."
                )

            if request.command == ConnectionCommand.CONNECT:
                self.controller.connect_bot(request.bot_name)
                return ConnectionCommandResult.ok(
                    "Bot conectado correctamente.",
                    request.bot_name,
                )

            if request.command == ConnectionCommand.DISCONNECT:
                self.controller.disconnect_bot(request.bot_name)
                return ConnectionCommandResult.ok(
                    "Bot desconectado correctamente.",
                    request.bot_name,
                )

            if request.command == ConnectionCommand.RECOVER:
                self.controller.recover_bot(request.bot_name)
                return ConnectionCommandResult.ok(
                    "Bot recuperado correctamente.",
                    request.bot_name,
                )

            if request.command == ConnectionCommand.STATUS:
                connected = self.controller.get_connected_bots()
                disconnected = self.controller.get_disconnected_bots()

                return ConnectionCommandResult.ok(
                    f"Conectados: {len(connected)} | "
                    f"Desconectados: {len(disconnected)}"
                )

            return ConnectionCommandResult.error(
                f"Comando no soportado: {request.command}"
            )

        except (KeyError, ValueError, RuntimeError) as exc:
            return ConnectionCommandResult.error(str(exc), request.bot_name)
