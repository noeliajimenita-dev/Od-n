from .bot import TelegramBot
from .command import TelegramCommand
from .default_handler import DefaultTelegramHandler
from .handler import TelegramHandler
from .message import TelegramMessage
from .response import TelegramResponse


class TelegramBotHandler:
    def __init__(
        self,
        bot: TelegramBot,
        handler: TelegramHandler | None = None,
    ):
        self.bot = bot
        self.handler = handler or DefaultTelegramHandler()

    def handle_message(
        self,
        chat_id: str,
        text: str,
    ) -> TelegramResponse:
        message = TelegramMessage.create(
            chat_id=chat_id,
            text=text,
            bot_name=self.bot.name,
        )

        return self.handler.handle_message(message)

    def handle_command(
        self,
        text: str,
    ) -> TelegramResponse:
        command = TelegramCommand.parse(text)

        if command is None:
            return TelegramResponse.error_response(
                bot_name=self.bot.name,
                text="El texto no contiene un comando válido.",
            )

        return self.handler.handle_command(command)
