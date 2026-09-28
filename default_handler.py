from .command import TelegramCommand
from .handler import TelegramHandler
from .message import TelegramMessage
from .response import TelegramResponse


class DefaultTelegramHandler(TelegramHandler):

    def handle_message(
        self,
        message: TelegramMessage,
    ) -> TelegramResponse:
        if message.is_empty():
            return TelegramResponse.error_response(
                bot_name=message.bot_name,
                text="El mensaje está vacío.",
            )

        return TelegramResponse.success_response(
            bot_name=message.bot_name,
            text="Mensaje recibido correctamente.",
        )

    def handle_command(
        self,
        command: TelegramCommand,
    ) -> TelegramResponse:
        return TelegramResponse.success_response(
            bot_name="system",
            text=f"Comando recibido: /{command.name}",
        )
